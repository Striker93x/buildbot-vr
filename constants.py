import yaml

with open('/srv/buildbot/master/os_info.yaml', 'r') as f:
    os_info = yaml.safe_load(f)

github_status_builders = [
        "amd64-centos-7",
        "amd64-debian-10",
        "amd64-fedora-35",
        "amd64-ubuntu-2004-clang11",
        "amd64-ubuntu-2004-debug",
        "amd64-windows",
        ]

release_builders = [
        "aarch64-centos-7",
        "aarch64-centos-7-rpm-autobake",
        "aarch64-debian-9",
        "aarch64-debian-9-deb-autobake",
        "aarch64-debian-10",
        "aarch64-debian-10-deb-autobake",
        "aarch64-debian-11",
        "aarch64-debian-11-deb-autobake",
        "aarch64-debian-sid",
        "aarch64-debian-sid-deb-autobake",
        "aarch64-fedora-34",
        "aarch64-fedora-34-rpm-autobake",
        "aarch64-fedora-35",
        "aarch64-fedora-35-rpm-autobake",
        "aarch64-rhel-8",
        "aarch64-rhel-8-rpm-autobake",
        "aarch64-ubuntu-1804",
        "aarch64-ubuntu-1804-deb-autobake",
        "aarch64-ubuntu-2110",
        "aarch64-ubuntu-2110-deb-autobake",
        "aarch64-ubuntu-2004",
        "aarch64-ubuntu-2004-deb-autobake",
        "amd64-debian-sid",
        "amd64-debian-sid-deb-autobake",
        "ppc64le-debian-11",
        "ppc64le-debian-11-deb-autobake",
        "ppc64le-debian-sid",
        "ppc64le-debian-sid-deb-autobake",
        "s390x-ubuntu-2004",
        "s390x-ubuntu-2004-deb-autobake",
        "s390x-ubuntu-2204",
        "s390x-ubuntu-2204-deb-autobake",
        "s390x-rhel-8",
        "s390x-rhel-8-rpm-autobake",
        "s390x-sles-15",
        "s390x-sles-15-rpm-autobake",
        ]

builders_autobake=["amd64-centos-7-rpm-autobake", "amd64-centos-stream8-rpm-autobake", "amd64-debian-9-deb-autobake", "x86-debian-9-deb-autobake", "amd64-debian-10-deb-autobake", "amd64-debian-11-deb-autobake", "amd64-debian-sid-deb-autobake", "x86-debian-sid-deb-autobake", "amd64-fedora-34-rpm-autobake", "amd64-fedora-35-rpm-autobake", "amd64-rhel-7-rpm-autobake", "amd64-rhel-8-rpm-autobake", "amd64-opensuse-15-rpm-autobake", "amd64-sles-12-rpm-autobake", "amd64-sles-15-rpm-autobake", "amd64-ubuntu-1804-deb-autobake", "amd64-ubuntu-2004-deb-autobake", "amd64-ubuntu-2110-deb-autobake", "amd64-ubuntu-2204-deb-autobake", "aarch64-ubuntu-1804-deb-autobake", "aarch64-ubuntu-2004-deb-autobake", "aarch64-ubuntu-2204-deb-autobake", "aarch64-ubuntu-2110-deb-autobake", "ppc64le-debian-9-deb-autobake", "ppc64le-debian-10-deb-autobake", "ppc64le-debian-11-deb-autobake", "ppc64le-debian-sid-deb-autobake", "ppc64le-ubuntu-1804-deb-autobake", "ppc64le-ubuntu-2004-deb-autobake", "ppc64le-ubuntu-2110-deb-autobake", "ppc64le-ubuntu-2204-deb-autobake", "ppc64le-centos-7-rpm-autobake", "ppc64le-rhel-7-rpm-autobake", "ppc64le-rhel-8-rpm-autobake", "aarch64-debian-10-deb-autobake", "aarch64-debian-11-deb-autobake", "aarch64-debian-sid-deb-autobake", "aarch64-debian-9-deb-autobake", "aarch64-fedora-34-rpm-autobake", "aarch64-fedora-35-rpm-autobake", "aarch64-centos-7-rpm-autobake", "aarch64-centos-8-rpm-autobake", "aarch64-rhel-7-rpm-autobake", "aarch64-rhel-8-rpm-autobake", "s390x-ubuntu-2004-deb-autobake", "s390x-ubuntu-2204-deb-autobake", "s390x-rhel-8-rpm-autobake", "s390x-sles-15-rpm-autobake"]

builders_big=["amd64-ubuntu-1804-bigtest"]

# Generate install builders based on the os_info data
builders_install = []
builders_upgrade = []
for os in os_info:
    for arch in os_info[os]['arch']:
        builder_name_install = arch + '-' + os + '-' + os_info[os]['type'] + '-autobake-install'
        builders_install.append(builder_name_install)
        builder_name_minor_upgrade = arch + '-' + os + '-' + os_info[os]['type'] + '-autobake-minor-upgrade'
        builders_upgrade.append(builder_name_minor_upgrade)
        builder_name_major_upgrade = arch + '-' + os + '-' + os_info[os]['type'] + '-autobake-major-upgrade'
        builders_upgrade.append(builder_name_major_upgrade)

builders_eco=["amd64-ubuntu-2004-eco-php", "amd64-debian-10-eco-pymysql", "amd64-debian-10-eco-mysqljs", "amd64-ubuntu-2004-eco-dbdeployer"]

builders_dockerlibrary=["amd64-rhel8-dockerlibrary"]

# Note:
# Maximum supported branch is the one where the default distro MariaDB package major version <= branch
# For example, if Debian 10 has MariaDB 10.3 by default, we don't support MariaDB 10.2 on it.
supportedPlatforms = {}
supportedPlatforms["10.2"] = ['aarch64-centos-7', 'aarch64-centos-8', 'aarch64-debian-10', 'aarch64-debian-9', 'aarch64-rhel-7', 'aarch64-rhel-8', 'aarch64-ubuntu-1804', 'amd64-centos-7', 'amd64-debian-10', 'amd64-debian-9', 'amd64-opensuse-15', 'amd64-rhel-7', 'amd64-rhel-8', 'amd64-ubuntu-1804', 'amd64-ubuntu-1804-clang10', 'amd64-ubuntu-1804-clang10-asan', 'amd64-ubuntu-1804-clang6', 'amd64-ubuntu-1804-valgrind', 'amd64-ubuntu-2004', 'amd64-ubuntu-2004-debug', 'amd64-ubuntu-2004-clang11', 'amd64-windows', 'ppc64le-centos-7', 'ppc64le-debian-9', 'ppc64le-rhel-7', 'ppc64le-rhel-8', 'ppc64le-ubuntu-1804', 'x86-debian-9', 'x86-ubuntu-1804']
supportedPlatforms["10.3"] = ['aarch64-centos-7', 'aarch64-centos-8', 'aarch64-debian-10', 'aarch64-debian-9', 'aarch64-rhel-7', 'aarch64-rhel-8', 'aarch64-ubuntu-1804', 'aarch64-ubuntu-2004', 'amd64-centos-7', 'amd64-centos-stream8', 'amd64-debian-10', 'amd64-debian-9', 'amd64-opensuse-15', 'amd64-rhel-7', 'amd64-rhel-8', 'amd64-ubuntu-1804', 'amd64-ubuntu-1804-clang10', 'amd64-ubuntu-1804-clang10-asan', 'amd64-ubuntu-1804-clang6', 'amd64-ubuntu-2004-debug', 'amd64-ubuntu-1804-valgrind', 'amd64-ubuntu-2004', 'amd64-ubuntu-2004-clang11', 'amd64-windows', 'ppc64le-centos-7', 'ppc64le-centos-8', 'ppc64le-debian-10', 'ppc64le-debian-9', 'ppc64le-rhel-7', 'ppc64le-rhel-8', 'ppc64le-ubuntu-1804', 'ppc64le-ubuntu-2004-clang1x', 'ppc64le-ubuntu-1804-without-server', 'ppc64le-ubuntu-2004', 'x86-debian-9', 'x86-debian-9-bintar-systemd', 'x86-debian-9-bintar-initd', 'amd64-debian-9-bintar-systemd', 'amd64-debian-9-bintar-initd', 'aarch64-centos-7-bintar-systemd', 'aarch64-centos-7-bintar-initd', 'ppc64le-debian-9-bintar-systemd', 'ppc64le-debian-9-bintar-initd']
supportedPlatforms["10.4"] = ['aarch64-centos-7', 'aarch64-centos-8', 'aarch64-debian-10', 'aarch64-debian-9', 'aarch64-rhel-7', 'aarch64-rhel-8', 'aarch64-ubuntu-1804', 'aarch64-ubuntu-2004', 'amd64-centos-7', 'amd64-centos-stream8', 'amd64-debian-10', 'amd64-debian-9', 'amd64-opensuse-15', 'amd64-rhel-7', 'amd64-rhel-8', 'amd64-ubuntu-1804', 'amd64-ubuntu-1804-clang10', 'amd64-ubuntu-1804-clang10-asan', 'amd64-ubuntu-1804-clang6', 'amd64-ubuntu-2004-debug', 'amd64-ubuntu-1804-valgrind', 'amd64-ubuntu-2004', 'amd64-ubuntu-2004-clang11', 'amd64-windows', 'ppc64le-centos-7', 'ppc64le-centos-8', 'ppc64le-debian-10', 'ppc64le-debian-9', 'ppc64le-rhel-7', 'ppc64le-rhel-8', 'ppc64le-ubuntu-1804', 'ppc64le-ubuntu-2004-clang1x', 'ppc64le-ubuntu-1804-without-server', 'ppc64le-ubuntu-2004', 'x86-debian-9', 'x86-debian-9-bintar-systemd', 'x86-debian-9-bintar-initd', 'amd64-debian-9-bintar-systemd', 'amd64-debian-9-bintar-initd', 'aarch64-centos-7-bintar-systemd', 'aarch64-centos-7-bintar-initd', 'ppc64le-debian-9-bintar-systemd', 'ppc64le-debian-9-bintar-initd']
supportedPlatforms["10.5"] = ['aarch64-centos-7', 'aarch64-centos-8', 'aarch64-debian-10', 'aarch64-debian-11', 'aarch64-debian-9', 'aarch64-debian-sid', 'aarch64-fedora-34', "aarch64-fedora-35", 'aarch64-rhel-7', 'aarch64-rhel-8', 'aarch64-ubuntu-1804', 'aarch64-ubuntu-2004', "aarch64-ubuntu-2110", 'amd64-centos-7', 'amd64-centos-stream8', 'amd64-debian-10', 'amd64-debian-11', 'amd64-debian-9', 'amd64-debian-sid', 'amd64-fedora-34', 'amd64-fedora-35', 'amd64-opensuse-15', 'amd64-rhel-7', 'amd64-rhel-8', 'amd64-ubuntu-1804', 'amd64-ubuntu-1804-clang10', 'amd64-ubuntu-1804-clang10-asan', 'amd64-ubuntu-1804-clang6', 'amd64-ubuntu-2004-debug', 'amd64-ubuntu-2004-msan', 'amd64-ubuntu-1804-valgrind', 'amd64-ubuntu-2004', 'amd64-ubuntu-2004-clang11', 'amd64-ubuntu-2004-fulltest', 'amd64-ubuntu-1804-icc', 'amd64-ubuntu-2110', 'amd64-windows', 'ppc64le-centos-7', 'ppc64le-debian-10', 'ppc64le-debian-11', 'ppc64le-debian-9', 'ppc64le-debian-sid', 'ppc64le-rhel-7', 'ppc64le-rhel-8', 'ppc64le-ubuntu-1804', 'ppc64le-ubuntu-2004-clang1x', 'ppc64le-ubuntu-1804-without-server', 'ppc64le-ubuntu-2004', 'ppc64le-ubuntu-2110', 'x86-debian-9', 'x86-debian-sid', 'x86-ubuntu-1804', 'x86-debian-9-bintar-systemd', 'x86-debian-9-bintar-initd', 'amd64-debian-9-bintar-systemd', 'amd64-debian-9-bintar-initd', 'aarch64-centos-7-bintar-systemd', 'aarch64-centos-7-bintar-initd', 'ppc64le-debian-9-bintar-systemd', 'ppc64le-debian-9-bintar-initd', 'aix', 's390x-ubuntu-2004', 's390x-rhel-8', 's390x-sles-15']
supportedPlatforms["10.6"] = ['aarch64-centos-7', 'aarch64-centos-8', 'aarch64-debian-10', 'aarch64-debian-11', 'aarch64-debian-9', 'aarch64-debian-sid', 'aarch64-fedora-34', "aarch64-fedora-35", 'aarch64-rhel-7', 'aarch64-rhel-8', 'aarch64-ubuntu-1804', 'aarch64-ubuntu-2004', "aarch64-ubuntu-2110", 'aarch64-ubuntu-2204', 'amd64-centos-7', 'amd64-centos-stream8', 'amd64-debian-10', 'amd64-debian-11', 'amd64-debian-9', 'amd64-debian-sid', 'amd64-fedora-34', 'amd64-fedora-35', 'amd64-opensuse-15', 'amd64-rhel-7', 'amd64-rhel-8', 'amd64-ubuntu-1804', 'amd64-ubuntu-1804-clang10', 'amd64-ubuntu-1804-clang10-asan', 'amd64-ubuntu-1804-clang6', 'amd64-ubuntu-2004-debug', 'amd64-ubuntu-2004-msan', 'amd64-ubuntu-1804-valgrind', 'amd64-ubuntu-2004', 'amd64-ubuntu-2004-clang11', 'amd64-ubuntu-2004-fulltest', 'amd64-ubuntu-1804-icc', 'amd64-ubuntu-2110', 'amd64-ubuntu-2204', 'amd64-windows', 'ppc64le-centos-7', 'ppc64le-debian-10', 'ppc64le-debian-11', 'ppc64le-debian-9', 'ppc64le-debian-sid', 'ppc64le-rhel-7', 'ppc64le-rhel-8', 'ppc64le-ubuntu-1804', 'ppc64le-ubuntu-2004-clang1x', 'ppc64le-ubuntu-1804-without-server', 'ppc64le-ubuntu-2004', 'ppc64le-ubuntu-2110', 'ppc64le-ubuntu-2204', 'x86-debian-9', 'x86-debian-sid', 'x86-ubuntu-1804', 'x86-debian-9-bintar-systemd', 'x86-debian-9-bintar-initd', 'amd64-debian-9-bintar-systemd', 'amd64-debian-9-bintar-initd', 'aarch64-centos-7-bintar-systemd', 'aarch64-centos-7-bintar-initd', 'ppc64le-debian-9-bintar-systemd', 'ppc64le-debian-9-bintar-initd', 'aix', 's390x-ubuntu-2004', 's390x-ubuntu-2204', 's390x-rhel-8', 's390x-sles-15']
supportedPlatforms["10.7"] = ['aarch64-centos-7', 'aarch64-centos-8', 'aarch64-debian-10', 'aarch64-debian-11', 'aarch64-debian-9', 'aarch64-debian-sid', 'aarch64-fedora-34', "aarch64-fedora-35", 'aarch64-rhel-7', 'aarch64-rhel-8', 'aarch64-ubuntu-1804', 'aarch64-ubuntu-2004', "aarch64-ubuntu-2110", 'aarch64-ubuntu-2204', 'amd64-centos-7', 'amd64-centos-stream8', 'amd64-debian-10', 'amd64-debian-11', 'amd64-debian-9', 'amd64-debian-sid', 'amd64-fedora-34', 'amd64-fedora-35', 'amd64-opensuse-15', 'amd64-rhel-7', 'amd64-rhel-8', 'amd64-ubuntu-1804', 'amd64-ubuntu-1804-clang10', 'amd64-ubuntu-1804-clang10-asan', 'amd64-ubuntu-1804-clang6', 'amd64-ubuntu-2004-debug', 'amd64-ubuntu-2004-msan', 'amd64-ubuntu-1804-valgrind', 'amd64-ubuntu-2004', 'amd64-ubuntu-2004-clang11', 'amd64-ubuntu-2004-fulltest', 'amd64-ubuntu-1804-icc', 'amd64-ubuntu-2110', 'amd64-ubuntu-2204', 'amd64-windows', 'ppc64le-centos-7', 'ppc64le-debian-10', 'ppc64le-debian-11', 'ppc64le-debian-9', 'ppc64le-debian-sid', 'ppc64le-rhel-7', 'ppc64le-rhel-8', 'ppc64le-ubuntu-1804', 'ppc64le-ubuntu-2004-clang1x', 'ppc64le-ubuntu-1804-without-server', 'ppc64le-ubuntu-2004', 'ppc64le-ubuntu-2110', 'ppc64le-ubuntu-2204', 'x86-debian-9', 'x86-debian-sid', 'x86-ubuntu-1804', 'x86-debian-9-bintar-systemd', 'x86-debian-9-bintar-initd', 'amd64-debian-9-bintar-systemd', 'amd64-debian-9-bintar-initd', 'aarch64-centos-7-bintar-systemd', 'aarch64-centos-7-bintar-initd', 'ppc64le-debian-9-bintar-systemd', 'ppc64le-debian-9-bintar-initd', 'aix', 's390x-ubuntu-2004', 's390x-ubuntu-2204', 's390x-rhel-8', 's390x-sles-15']
supportedPlatforms["10.8"] = ['aarch64-centos-7', 'aarch64-centos-8', 'aarch64-debian-10', 'aarch64-debian-11', 'aarch64-debian-9', 'aarch64-debian-sid', 'aarch64-fedora-34', "aarch64-fedora-35", 'aarch64-rhel-7', 'aarch64-rhel-8', 'aarch64-ubuntu-1804', 'aarch64-ubuntu-2004', "aarch64-ubuntu-2110", 'aarch64-ubuntu-2204', 'amd64-centos-7', 'amd64-centos-stream8', 'amd64-debian-10', 'amd64-debian-11', 'amd64-debian-9', 'amd64-debian-sid', 'amd64-fedora-34', 'amd64-fedora-35', 'amd64-opensuse-15', 'amd64-rhel-7', 'amd64-rhel-8', 'amd64-ubuntu-1804', 'amd64-ubuntu-1804-clang10', 'amd64-ubuntu-1804-clang10-asan', 'amd64-ubuntu-1804-clang6', 'amd64-ubuntu-2004-debug', 'amd64-ubuntu-2004-msan', 'amd64-ubuntu-1804-valgrind', 'amd64-ubuntu-2004', 'amd64-ubuntu-2004-clang11', 'amd64-ubuntu-2004-fulltest', 'amd64-ubuntu-1804-icc', 'amd64-ubuntu-2110', 'amd64-ubuntu-2204', 'amd64-windows', 'ppc64le-centos-7', 'ppc64le-debian-10', 'ppc64le-debian-11', 'ppc64le-debian-9', 'ppc64le-debian-sid', 'ppc64le-rhel-7', 'ppc64le-rhel-8', 'ppc64le-ubuntu-1804', 'ppc64le-ubuntu-2004-clang1x', 'ppc64le-ubuntu-1804-without-server', 'ppc64le-ubuntu-2004', 'ppc64le-ubuntu-2110', 'ppc64le-ubuntu-2204', 'x86-debian-9', 'x86-debian-sid', 'x86-ubuntu-1804', 'x86-debian-9-bintar-systemd', 'x86-debian-9-bintar-initd', 'amd64-debian-9-bintar-systemd', 'amd64-debian-9-bintar-initd', 'aarch64-centos-7-bintar-systemd', 'aarch64-centos-7-bintar-initd', 'ppc64le-debian-9-bintar-systemd', 'ppc64le-debian-9-bintar-initd', 'aix', 's390x-ubuntu-2004', 's390x-ubuntu-2204', 's390x-rhel-8', 's390x-sles-15']
supportedPlatforms["10.9"] = ['aarch64-centos-7', 'aarch64-centos-8', 'aarch64-debian-10', 'aarch64-debian-11', 'aarch64-debian-9', 'aarch64-debian-sid', 'aarch64-fedora-34', "aarch64-fedora-35", 'aarch64-rhel-7', 'aarch64-rhel-8', 'aarch64-ubuntu-1804', 'aarch64-ubuntu-2004', "aarch64-ubuntu-2110", 'aarch64-ubuntu-2204', 'amd64-centos-7', 'amd64-centos-stream8', 'amd64-debian-10', 'amd64-debian-11', 'amd64-debian-9', 'amd64-debian-sid', 'amd64-fedora-34', 'amd64-fedora-35', 'amd64-opensuse-15', 'amd64-rhel-7', 'amd64-rhel-8', 'amd64-ubuntu-1804', 'amd64-ubuntu-1804-clang10', 'amd64-ubuntu-1804-clang10-asan', 'amd64-ubuntu-1804-clang6', 'amd64-ubuntu-2004-debug', 'amd64-ubuntu-2004-msan', 'amd64-ubuntu-1804-valgrind', 'amd64-ubuntu-2004', 'amd64-ubuntu-2004-clang11', 'amd64-ubuntu-2004-fulltest', 'amd64-ubuntu-1804-icc', 'amd64-ubuntu-2110', 'amd64-ubuntu-2204', 'amd64-windows', 'ppc64le-centos-7', 'ppc64le-debian-10', 'ppc64le-debian-11', 'ppc64le-debian-9', 'ppc64le-debian-sid', 'ppc64le-rhel-7', 'ppc64le-rhel-8', 'ppc64le-ubuntu-1804', 'ppc64le-ubuntu-2004-clang1x', 'ppc64le-ubuntu-1804-without-server', 'ppc64le-ubuntu-2004', 'ppc64le-ubuntu-2110', 'ppc64le-ubuntu-2204', 'x86-debian-9', 'x86-debian-sid', 'x86-ubuntu-1804', 'x86-debian-9-bintar-systemd', 'x86-debian-9-bintar-initd', 'amd64-debian-9-bintar-systemd', 'amd64-debian-9-bintar-initd', 'aarch64-centos-7-bintar-systemd', 'aarch64-centos-7-bintar-initd', 'ppc64le-debian-9-bintar-systemd', 'ppc64le-debian-9-bintar-initd', 'aix', 's390x-ubuntu-2004', 's390x-ubuntu-2204', 's390x-rhel-8', 's390x-sles-15']
supportedPlatforms["10.10"] = ['aarch64-centos-7', 'aarch64-centos-8', 'aarch64-debian-10', 'aarch64-debian-11', 'aarch64-debian-9', 'aarch64-debian-sid', 'aarch64-fedora-34', "aarch64-fedora-35", 'aarch64-rhel-7', 'aarch64-rhel-8', 'aarch64-ubuntu-1804', 'aarch64-ubuntu-2004', "aarch64-ubuntu-2110", 'aarch64-ubuntu-2204', 'amd64-centos-7', 'amd64-centos-stream8', 'amd64-debian-10', 'amd64-debian-11', 'amd64-debian-9', 'amd64-debian-sid', 'amd64-fedora-34', 'amd64-fedora-35', 'amd64-opensuse-15', 'amd64-rhel-7', 'amd64-rhel-8', 'amd64-ubuntu-1804', 'amd64-ubuntu-1804-clang10', 'amd64-ubuntu-1804-clang10-asan', 'amd64-ubuntu-1804-clang6', 'amd64-ubuntu-2004-debug', 'amd64-ubuntu-2004-msan', 'amd64-ubuntu-1804-valgrind', 'amd64-ubuntu-2004', 'amd64-ubuntu-2004-clang11', 'amd64-ubuntu-2004-fulltest', 'amd64-ubuntu-1804-icc', 'amd64-ubuntu-2110', 'amd64-ubuntu-2204', 'amd64-windows', 'ppc64le-centos-7', 'ppc64le-debian-10', 'ppc64le-debian-11', 'ppc64le-debian-9', 'ppc64le-debian-sid', 'ppc64le-rhel-7', 'ppc64le-rhel-8', 'ppc64le-ubuntu-1804', 'ppc64le-ubuntu-2004-clang1x', 'ppc64le-ubuntu-1804-without-server', 'ppc64le-ubuntu-2004', 'ppc64le-ubuntu-2110', 'ppc64le-ubuntu-2204', 'x86-debian-9', 'x86-debian-sid', 'x86-ubuntu-1804', 'x86-debian-9-bintar-systemd', 'x86-debian-9-bintar-initd', 'amd64-debian-9-bintar-systemd', 'amd64-debian-9-bintar-initd', 'aarch64-centos-7-bintar-systemd', 'aarch64-centos-7-bintar-initd', 'ppc64le-debian-9-bintar-systemd', 'ppc64le-debian-9-bintar-initd', 'aix', 's390x-ubuntu-2004', 's390x-ubuntu-2204', 's390x-rhel-8', 's390x-sles-15']

# Hack to remove all github_status_builders since they are triggered separately
for k in supportedPlatforms:
    supportedPlatforms[k] = list(filter(lambda x: x not in github_status_builders, supportedPlatforms[k]))

DEVELOPMENT_BRANCH="10.10"
RELEASABLE_BRANCHES="5.5 10.0 10.1 10.2 10.3 10.4 10.5 10.6 bb-5.5-release bb-10.0-release bb-10.1-release bb-10.2-release bb-10.3-release bb-10.4-release bb-10.5-release bb-10.6-release"
savedPackageBranches= ["5.5", "10.0", "10.1", "10.2", "10.3", "10.4", "10.5", "10.6", "10.7", "10.8", "10.9", "10.10", "bb-*-release", "bb-10.2-compatibility", "preview-*"]
# The trees for which we save binary packages.
releaseBranches = ["bb-*-release", "preview-10.*"]
