#!/usr/bin/env bash
# shellcheck disable=SC2154

# Include with:
# . ./bash_lib.sh

bb_log_info() {
  set +x
  echo >&1 "INFO: $*"
  set -x
}

bb_log_warn() {
  set +x
  echo >&1 "WARNING: $*"
  set -x
}

bb_log_skip() {
  set +x
  echo >&1 "SKIP: $*"
  set -x
}

bb_log_err() {
  set +x
  echo >&2 "ERROR: $*"
  set -x
}

bb_log_ok() {
  set +x
  echo >&1 "OK: $*"
  set -x
}

err() {
  set +x
  echo >&2 "ERROR: $*"
  exit 1
}

manual_run_switch() {
  # check if we are in Buildbot CI or not
  if [[ $BB_CI != "True" ]]; then
    if [[ -z $1 ]]; then
      echo "Please provide the build URL, example:"
      echo "$0 https://buildbot.mariadb.org/#/builders/171/builds/7351"
      exit 1
    else
      # define environment variables from build properties
      for cmd in jq wget; do
        command -v $cmd >/dev/null ||
          err "$cmd command not found"
      done
      # get buildid
      buildid=$(wget -qO- "${1/\#/api/v2}" | jq -r '.builds[] | .buildid')
      # get build properties
      wget -q "https://buildbot.mariadb.org/api/v2/builds/$buildid/properties" -O properties.json ||
        err "unable to get build properties from $1"
      # //TEMP do better with jq filtering
      for var in $(jq -r '.properties[]' properties.json | grep -v warnings-count | grep ": \[" | cut -d \" -f2); do
        export "$var"="$(jq -r ".properties[] | .${var}[0]" properties.json)"
      done
      # we need some global env vars (not provided as properties)
      wget -q "https://raw.githubusercontent.com/MariaDB/buildbot/main/constants.py" -O constants.py ||
        err "unable to get global env vars"
      dev_branch=$(grep DEVELOPMENT_BRANCH constants.py | cut -d \" -f2)
      export development_branch="$dev_branch"
    fi
    # for RPM we have to download artifacts from ci.mariadb.org
    if command -v rpm >/dev/null; then
      mkdir rpms
      wget -r -np -nH --cut-dirs=3 -A "*.rpm" "https://ci.mariadb.org/$tarbuildnum/$parentbuildername/rpms" -P rpms
    fi
  fi
}

bb_print_env() {
  # Environment
  source /etc/os-release
  echo -e "\nDistribution: $PRETTY_NAME"
  echo "Architecture: $arch"
  echo -e "Systemd capability: $systemdCapability"
  echo "MariaDB version: ${mariadb_version/mariadb-/}"
  if [[ $test_type == "major" ]]; then
    echo "MariaDB previous major version: $prev_major_version"
  fi
  echo -e "\nKernel:"
  uname -a
  echo -e "\nUlimits:"
  ulimit -a
  echo -e "\nDisk usage:"
  df -kT

  # make sure SELinux is in Enforcing mode
  if [[ -f /etc/selinux/config ]]; then
    selinux_status=$(getenforce)
    if [[ $selinux_status != "Enforcing" ]]; then
      bb_log_warn "Selinux is not in enforcing mode ($selinux_status)"
    else
      echo -e "\nSelinux status: $selinux_status"
    fi
  fi

  if command -v dpkg >/dev/null; then
    package_manager="dpkg -l"
  else
    package_manager="rpm -qa"
  fi
  echo -e "\nMariaDB related packages installed (should be empty):"
  $package_manager | grep -iE 'maria|mysql|galera' || true
  echo ""
}

apt_get_update() {
  bb_log_info "update apt cache"
  res=1
  for i in {1..10}; do
    if sudo apt-get update; then
      res=0
      break
    fi
    bb_log_warn "apt-get update failed, retrying ($i)"
    sleep 5
  done

  if ((res != 0)); then
    bb_log_err "apt-get update failed"
    exit $res
  fi
}

yum_makecache() {
  # Try several times, to avoid sporadic "The requested URL returned error: 404"
  made_cache=0
  for i in {1..5}; do
    sudo rm -rf /var/cache/yum/*
    sudo yum clean all
    source /etc/os-release
    if [[ $ID == "rhel" ]]; then
      sudo subscription-manager refresh
    fi
    if sudo yum makecache; then
      made_cache=1
      break
    else
      bb_log_info "try several times ($i), to avoid sporadic The requested URL returned error: 404"
      sleep 5
    fi
  done

  if ((made_cache != 1)); then
    bb_log_err "failed to make cache"
    exit 1
  fi
}

wait_for_mariadb_upgrade() {
  res=1
  for i in {1..20}; do
    if pgrep -i 'mysql_upgrade|mysqlcheck|mysqlrepair|mysqlanalyze|mysqloptimize|mariadb-upgrade|mariadb-check'; then
      bb_log_info "wait for mysql_upgrade to finish ($i)"
      sleep 5
    else
      res=0
      break
    fi
  done
  if ((res != 0)); then
    bb_log_err "mysql_upgrade or alike have not finished in reasonable time"
    exit $res
  fi
}

deb_setup_mariadb_mirror() {
  # stop if any further variable is undefined
  set -u
  [[ -n $1 ]] || {
    bb_log_err "missing the branch variable"
    exit 1
  }
  branch=$1
  if [[ $branch == "$development_branch" ]]; then
    #TOFIX - temp hack
    prev_released=$((${branch/1[0-9]./} - 1))
    if (( prev_released < 0 )); then
      branch="10.11"
    else
      branch="10.$prev_released"
    fi
    bb_log_info "using previous $branch released version for development branch $1"
  fi
  bb_log_info "setup MariaDB repository for $branch branch"
  command -v wget >/dev/null || {
    bb_log_err "wget command not found"
    exit 1
  }
  # 10.2 is EOL and only on archive.mariadb.org
  if [[ $branch == "10.2" ]]; then
    mirror="https://archive.mariadb.org/mariadb-10.2/repo"
  else
    mirror="https://deb.mariadb.org/$branch"
  fi
  if wget -q --spider "$mirror/$dist_name/dists/$version_name"; then
    sudo sh -c "echo 'deb $mirror/$dist_name $version_name main' >/etc/apt/sources.list.d/mariadb.list"
    sudo wget https://mariadb.org/mariadb_release_signing_key.asc -O /etc/apt/trusted.gpg.d/mariadb_release_signing_key.asc || {
      bb_log_err "mariadb repository key installation failed"
      exit 1
    }
  else
    bb_log_err "deb_setup_mariadb_mirror: $branch packages for $dist_name $version_name does not exist on https://deb.mariadb.org/"
    exit 1
  fi
  set +u
}

deb_setup_bb_artifacts_mirror() {
  # stop if any variable is undefined
  set -u
  bb_log_info "setup buildbot artifact repository"
  sudo sh -c "echo 'deb [trusted=yes] https://ci.mariadb.org/$tarbuildnum/$parentbuildername/debs ./' >/etc/apt/sources.list.d/bb-artifacts.list"
  set +u
}

upgrade_type_mode() {
  case "$branch" in
    *galera*)
      if [[ $test_mode == "all" ]]; then
        bb_log_warn "the test in 'all' mode is not executed for galera branches"
        exit
      fi
      ;;
    "$development_branch")
      if [[ $test_mode != "server" ]]; then
        bb_log_warn "for non-stable branches the test is only run in 'test' mode"
        exit
      fi
      ;;
  esac
}

upgrade_test_type() {
  case $1 in
    "minor")
      prev_major_version=$major_version
      ;;
    "major")
      #TOFIX - temp hack
      minor_version=${major_version/1[0-9]./}
      if (( minor_version == 0 )); then
        prev_minor_version=11
      else
        prev_minor_version=$((minor_version - 1))
      fi
      prev_major_version="10.$prev_minor_version"
      ;;
    *)
      bb_log_err "test type not provided"
      exit 1
      ;;
  esac
}

check_mariadb_server_and_create_structures() {
  if [ "$prev_major_version" != 10.3 ]; then
    # 10.4+ uses unix_socket by default
    sudo mysql -e "set password=password('rootpass')"
  else
    # Even without unix_socket, on some of VMs the password might be not pre-created as expected. This command should normally fail.
    mysql -uroot -e "set password = password('rootpass')" >>/dev/null 2>&1
  fi

  # All the commands below should succeed
  set -e
  mysql -uroot -prootpass -e "CREATE DATABASE db"
  mysql -uroot -prootpass -e "CREATE TABLE db.t_innodb(a1 SERIAL, c1 CHAR(8)) ENGINE=InnoDB; INSERT INTO db.t_innodb VALUES (1,'foo'),(2,'bar')"
  mysql -uroot -prootpass -e "CREATE TABLE db.t_myisam(a2 SERIAL, c2 CHAR(8)) ENGINE=MyISAM; INSERT INTO db.t_myisam VALUES (1,'foo'),(2,'bar')"
  mysql -uroot -prootpass -e "CREATE TABLE db.t_aria(a3 SERIAL, c3 CHAR(8)) ENGINE=Aria; INSERT INTO db.t_aria VALUES (1,'foo'),(2,'bar')"
  mysql -uroot -prootpass -e "CREATE TABLE db.t_memory(a4 SERIAL, c4 CHAR(8)) ENGINE=MEMORY; INSERT INTO db.t_memory VALUES (1,'foo'),(2,'bar')"
  mysql -uroot -prootpass -e "CREATE ALGORITHM=MERGE VIEW db.v_merge AS SELECT * FROM db.t_innodb, db.t_myisam, db.t_aria"
  mysql -uroot -prootpass -e "CREATE ALGORITHM=TEMPTABLE VIEW db.v_temptable AS SELECT * FROM db.t_innodb, db.t_myisam, db.t_aria"
  mysql -uroot -prootpass -e "CREATE PROCEDURE db.p() SELECT * FROM db.v_merge"
  mysql -uroot -prootpass -e "CREATE FUNCTION db.f() RETURNS INT DETERMINISTIC RETURN 1"
  if [[ $test_mode == "columnstore" ]]; then
    if ! mysql -uroot -prootpass -e "CREATE TABLE db.t_columnstore(a INT, c VARCHAR(8)) ENGINE=ColumnStore; SHOW CREATE TABLE db.t_columnstore; INSERT INTO db.t_columnstore VALUES (1,'foo'),(2,'bar')"; then
      get_columnstore_logs
      exit 1
    fi
  fi
  set +e
}

check_mariadb_server_and_verify_structures() {
  # Print "have_xx" capabilitites for the new server
  mysql -uroot -prootpass -e "select 'Stat' t, variable_name name, variable_value val from information_schema.global_status where variable_name like '%have%' union select 'Vars' t, variable_name name, variable_value val from information_schema.global_variables where variable_name like '%have%' order by t, name"
  # All the commands below should succeed
  set -e
  mysql -uroot -prootpass -e "select @@version, @@version_comment"
  mysql -uroot -prootpass -e "SHOW TABLES IN db"
  mysql -uroot -prootpass -e "SELECT * FROM db.t_innodb; INSERT INTO db.t_innodb VALUES (3,'foo'),(4,'bar')"
  mysql -uroot -prootpass -e "SELECT * FROM db.t_myisam; INSERT INTO db.t_myisam VALUES (3,'foo'),(4,'bar')"
  mysql -uroot -prootpass -e "SELECT * FROM db.t_aria; INSERT INTO db.t_aria VALUES (3,'foo'),(4,'bar')"
  bb_log_info "If the next INSERT fails with a duplicate key error,"
  bb_log_info "it is likely because the server was not upgraded or restarted after upgrade"
  mysql -uroot -prootpass -e "SELECT * FROM db.t_memory; INSERT INTO db.t_memory VALUES (1,'foo'),(2,'bar')"
  mysql -uroot -prootpass -e "SELECT COUNT(*) FROM db.v_merge"
  mysql -uroot -prootpass -e "SELECT COUNT(*) FROM db.v_temptable"
  mysql -uroot -prootpass -e "CALL db.p()"
  mysql -uroot -prootpass -e "SELECT db.f()"

  if [[ $test_mode == "columnstore" ]]; then
    if ! mysql -uroot -prootpass -e "SELECT * FROM db.t_columnstore; INSERT INTO db.t_columnstore VALUES (3,'foo'),(4,'bar')"; then
      get_columnstore_logs
      exit 1
    fi
  fi
  set +e
}

control_mariadb_server() {
  bb_log_info "$1 MariaDB server"
  case "$systemdCapability" in
    yes)
      sudo systemctl "$1" mariadb
      ;;
    no)
      sudo /etc/init.d/mysql "$1"
      ;;
  esac
}

store_mariadb_server_info() {
  mysql -uroot -prootpass --skip-column-names -e "select @@version" | awk -F'-' '{ print $1 }' >"/tmp/version.$1"
  mysql -uroot -prootpass --skip-column-names -e "select engine, support, transactions, savepoints from information_schema.engines" | sort >"/tmp/engines.$1"
  mysql -uroot -prootpass --skip-column-names -e "select plugin_name, plugin_status, plugin_type, plugin_library, plugin_license from information_schema.all_plugins" | sort >"/tmp/plugins.$1"
}

check_upgraded_versions() {
  for file in /tmp/version.old /tmp/version.new; do
    [[ -f $file ]] || {
      bb_log_err "$file not found"
      exit 1
    }
  done
  # check that a major upgrade was done
  if [[ $test_type == "major" ]]; then
    old_major_digit_incr=$(($(cut -d "." -f2 /tmp/version.old) + 1))
    new_major_digit=$(cut -d "." -f2 /tmp/version.new)
    ((old_major_digit_incr == new_major_digit)) || {
      bb_log_err "This does not look like a major upgrade:"
      diff -u /tmp/version.old /tmp/version.new
      exit 1
    }
  fi
  if diff -u /tmp/version.old /tmp/version.new; then
    bb_log_err "server version has not changed after upgrade"
    bb_log_err "it can be a false positive if we forgot to bump version after release,"
    bb_log_err "or if it is a development tree that is based on an old version"
    exit 1
  fi
}
