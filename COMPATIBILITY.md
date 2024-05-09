# Compatibility

Which Ansible role is proven to run on which OS?

```
                                     |    Debian    |   RHEL    |                Ubuntu                 | other
Role                                 | 10 | 11 | 12 | 7 | 8 | 9 | 16.04 | 18.04 | 20.04 | 22.04 | 24.04 |
-------------------------------------+----+----+----+---+---+---+-------+-------+-------+-------+-------+-----------
acme_sh                              |    |    |    |   | x |   |       |       |       |       |       |
ansible_init                         |    |    |    |   |   |   |       |       |       |       |       | Fedora 35+
apache_httpd                         |    |    |    |   | x | x |       |       |       |       |       |
apache_solr                          |    |    |    |   | x | x |       |       |       |       |       |
apache_tomcat                        |    |    |    | x | x |   |       |       |       |       |       |
apps                                 |    |    |    |   | x | x |       |       |       |       |       |
at                                   |    |    |    |   | x | x |   x   |       |       |       |       | Fedora 35
audit                                |    |    |    | x | x | x |       |       |       |       |       |
bind                                 |    |    |    |   | x | x |       |       |       |       |       |
borg_local                           |    |    |    | x | x |   |       |       |       |       |       |
chrony                               |    |    |    | x | x | x |       |       |       |       |       |
clamav                               |    |    |    |   | x |   |       |       |       |       |       |
cloud_init                           |    |    |    |   | x | x |   x   |       |       |       |       |
cockpit                              |    |    |    |   | x | x |   x   |       |       |       |       | Fedora 35
collabora                            |    |    |    |   | x |   |       |       |       |       |       |
coturn                               |    |    |    |   | x |   |       |       |       |       |       |
crypto_policy                        |    |    |    |   | x | x |       |       |       |       |       |
dnf_makecache                        |    |    |    |   | x | x |       |       |       |       |       |
dnf_versionlock                      |    |    |    | x | x |   |       |       |       |       |       |
docker                               |    |    |    |   | x |   |       |       |       |       |       |
duplicity                            |    |    |    | x | x | x |       |       |       |       |       | Fedora 35
elasticsearch_oss                    |    |    |    |   | x |   |       |       |       |       |       |
exoscale_vm                          |    |    |    |   |   |   |       |       |       |       |       | Fedora 35+
fail2ban                             |    |    |    |   | x |   |       |       |       |       |       |
fangfrisch                           |    |    |    |   | x |   |       |       |       |       |       |
files                                |    |    |    |   | x |   |       |       |       |       |       |
firewall                             |    |    |    | x | x | x |   x   |       |       |       |       |
freeipa_client                       |    |    |    | x | x |   |       |       |       |       |       |
freeipa_server                       |    |    |    |   | x |   |       |       |       |       |       |
github_project_createrepo            |    |    |    |   | x |   |       |       |       |       |       |
gitlab_ce                            |    |    |    |   | x |   |       |       |       |       |       |
glances                              |    |    |    |   | x | x |   x   |       |       |       |       |
grafana                              |    |    |    |   | x | x |       |       |       |       |       |
grafana_grizzly                      |    |    |    |   | x | x |       |       |       |       |       |
grav                                 |    |    |    |   | x |   |       |       |       |       |       |
graylog_server                       |    | x  |    |   | x |   |       |       |       |       |       |
haveged                              |    |    |    |   | x | x |       |       |       |       |       |
hetzner_vm                           |    |    |    |   |   |   |       |       |       |       |       | Fedora 35+
hostname                             |    |    |    |   | x | x |   x   |       |       |       |       |
-------------------------------------+----+----+----+---+---+---+-------+-------+-------+-------+-------+-----------
                                     |    Debian    |   RHEL    |                Ubuntu                 | other
Role                                 | 10 | 11 | 12 | 7 | 8 | 9 | 16.04 | 18.04 | 20.04 | 22.04 | 24.04 |
-------------------------------------+----+----+----+---+---+---+-------+-------+-------+-------+-------+-----------
icinga2_agent                        |    |    |    | x | x |   |       |       |       |       |       | Fedora 35
icinga2_master                       |    |    |    |   | x | x |       |       |       |       |       |
icingadb                             |    |    |    |   | x | x |       |       |       |       |       |
icingaweb2                           |    |    |    |   | x | x |       |       |       |       |       |
icingaweb2_module_businessprocess    |    |    |    |   | x | x |       |       |       |       |       |
icingaweb2_module_company            |    |    |    |   | x | x |       |       |       |       |       |
icingaweb2_module_director           |    |    |    |   | x | x |       |       |       |       |       |
icingaweb2_module_doc                |    |    |    |   | x | x |       |       |       |       |       |
icingaweb2_module_grafana            |    |    |    |   | x | x |       |       |       |       |       |
icingaweb2_module_incubator          |    |    |    |   | x | x |       |       |       |       |       |
icingaweb2_module_monitoring         |    |    |    |   | x | x |       |       |       |       |       |
icingaweb2_module_vspheredb          |    |    |    |   | x | x |       |       |       |       |       |
icingaweb2_module_x509               |    |    |    |   | x | x |       |       |       |       |       |
influxdb                             |    |    |    |   | x | x |       |       |       |       |       |
infomaniak_vm                        |    |    |    |   |   |   |       |       |       |       |       | Fedora 35+
kdump                                |    |    |    |   | x | x |   x   |       |       |       |       |
keepalived                           |    |    |    |   | x |   |       |       |       |       |       |
kernel_settings                      | -  | -  | -  |   | x | x |   -   |   -   |   -   |       |       |
keycloak                             |    |    |    |   | x |   |       |       |       |       |       |
kvm_host                             |    |    |    |   | x |   |       |       |       |       |       |
kvm_vm                               |    |    |    |   | x |   |       |       |       |       |       |
libmaxminddb                         |    |    |    |   | x |   |       |       |       |       |       |
librenms                             |    |    |    |   | x |   |       |       |       |       |       |
libreoffice                          |    |    |    |   | x |   |       |       |       |       |       |
login                                |    |    |    |   | x | x |   x   |       |       |       |       | Fedora 35+
logrotate                            |    |    |    | x | x | x |   x   |       |       |       |       | Fedora
mailto_root                          |    |    |    | x | x | x |   x   |       |       |       |       |
mailx                                | x  | x  | x  | x | x | x |   x   |       |       |       |       | Fedora
mariadb_client                       |    |    |    |   | x | x |       |       |       |       |       |
mariadb_server                       | -  | -  | -  |   | x | x |   -   |   -   |   -   |       |       |
maxmind_geoip                        |    |    |    |   | x |   |       |       |       |       |       |
minio_client                         |    |    |    |   | x |   |       |       |       |       |       |
mirror                               |    |    |    |   | x |   |       |       |       |       |       |
mod_maxminddb                        |    |    |    |   | x |   |       |       |       |       |       |
mongodb                              |    | x  |    |   | x | x |       |       |       |       |       |
monitoring_plugins                   | x  |    |    | x | x | x |   x   |       |       |       |       | Debian 9, Fedora, Suse, Windows
monitoring_plugins_grafana_dashboards|    |    |    |   | x | x |       |       |       |       |       |
motd                                 |    |    |    | x | x | x |   x   |       |       |       |       |
mount                                |    | x  |    | x | x | x |       |       |       |       |       |
network                              |    |    |    | x | x | x |       |       |       |       |       |
-------------------------------------+----+----+----+---+---+---+-------+-------+-------+-------+-------+-----------
                                     |    Debian    |   RHEL    |                Ubuntu                 | other
Role                                 | 10 | 11 | 12 | 7 | 8 | 9 | 16.04 | 18.04 | 20.04 | 22.04 | 24.04 |
-------------------------------------+----+----+----+---+---+---+-------+-------+-------+-------+-------+-----------
nextcloud                            |    |    |    |   | x |   |       |       |       |       |       |
nfs_client                           |    | x  |    | x | x | x |       |       |       |       |       |
nfs_server                           |    | x  |    | x | x |   |       |       |       |       |       |
nodejs                               |    |    |    |   | x | x |       |       |       |       |       |
objectstore_backup                   |    |    |    |   | x |   |       |       |       |       |       |
opensearch                           |    | x  |    |   | x |   |       |       |       |       |       |
openssl                              |    | x  |    |   | x | x |   x   |       |       |       |       |
open_vm_tools                        |    |    |    |   | x | x |   x   |       |       |       |       |
openvpn_server                       |    |    |    |   | x |   |       |       |       |       |       |
perl                                 |    |    |    |   | x | x |   x   |       |       |       |       |
php                                  |    |    |    |   | x | x |       |       |       |       |       |
policycoreutils                      |    |    |    | x | x | x |       |       |       |       |       | Fedora 35
postfix                              | x  | x  | x  | x | x | x |   x   |       |       |       |       | Fedora 35
postgresql_server                    |    |    |    |   | x |   |       |       |       |       |       |
python                               |    |    |    |   | x | x |   x   |       |       |       |       | Windows
python_venv                          |    | x  | x  | x | x | x |       |       |       |       |       | Fedora 35
qemu_guest_agent                     |    |    |    |   | x |   |   x   |       |       |       |       |
redis                                |    |    |    |   | x |   |       |       |       |       |       |
repo_baseos                          |    |    |    | x | x | x |       |       |       |       |       |
repo_collabora                       |    |    |    | x | x |   |       |       |       |       |       |
repo_collabora_code                  |    |    |    | x | x |   |       |       |       |       |       |
repo_debian_base                     | x  | x  |    |   |   |   |       |       |       |       |       |
repo_docker                          |    |    |    |   | x |   |       |       |       |       |       |
repo_elasticsearch                   |    |    |    |   | x |   |       |       |       |       |       |
repo_elasticsearch_oss               |    |    |    |   | x |   |       |       |       |       |       |
repo_epel                            |    |    |    | x | x | x |       |       |       |       |       |
repo_gitlab_ce                       |    |    |    |   | x |   |       |       |       |       |       |
repo_gitlab_runner                   |    |    |    |   | x |   |       |       |       |       |       |
repo_grafana                         |    |    |    |   | x |   |       |       |       |       |       |
repo_graylog                         |    | x  |    |   | x |   |       |       |       |       |       |
repo_icinga                          |    |    |    | x | x | x |       |       |       |       |       |
repo_influxdb                        |    | x  |    | x | x | x |       |       |       |       |       |
repo_mariadb                         |    |    |    | x | x | x |       |       |       |       |       |
repo_mongodb                         |    | x  |    |   | x | x |       |       |       |       |       |
repo_monitoring_plugins              | x  | x  |    | x | x | x |       |   x   |   x   |       |       | Ubuntu 22.04
repo_mydumper                        |    |    |    | x | x | x |       |       |       |       |       |
repo_opensearch                      |    | x  |    |   | x |   |       |       |       |       |       |
repo_postgresql                      |    |    |    |   | x |   |       |       |       |       |       |
repo_remi                            |    |    |    | x | x | x |       |       |       |       |       | Fedora 35
repo_rpmfusion                       |    |    |    |   | x |   |       |       |       |       |       |
-------------------------------------+----+----+----+---+---+---+-------+-------+-------+-------+-------+-----------
                                     |    Debian    |   RHEL    |                Ubuntu                 | other
Role                                 | 10 | 11 | 12 | 7 | 8 | 9 | 16.04 | 18.04 | 20.04 | 22.04 | 24.04 |
-------------------------------------+----+----+----+---+---+---+-------+-------+-------+-------+-------+-----------
repo_sury                            | x  | x  |    | - | - | - |       |       |       |       |       |
rocketchat                           |    |    |    | x | x |   |       |       |       |       |       | Fedora 35
rsyslog                              |    |    |    |   | x | x |       |       |       |       |       |
selinux                              |    |    |    |   | x | x |       |       |       |       |       |
snmp                                 |    |    |    | x | x | x |       |       |       |       |       |
sshd                                 |    |    |    |   | x | x |       |       |       |       |       |
system_update                        |    | x  | x  | x | x | x |       |       |       |       |       |
systemd_journald                     |    |    |    |   | x | x |       |       |       |       |       |
systemd_unit                         |    |    |    |   | x | x |       |       |       |       |       |
tar                                  |    |    |    |   | x | x |   x   |       |       |       |       |
telegraf                             |    |    |    |   | x |   |       |       |       |       |       |
timezone                             |    |    |    | x | x | x |   x   |       |       |       |       | Fedora 35
tools                                |    |    |    | x | x | x |       |       |       |       |       | Fedora
unattended_upgrades                  |    | x  |    |   |   |   |   x   |       |       |       |       |
vsftpd                               |    |    |    |   | x |   |       |       |       |       |       |
wordpress                            |    |    |    |   | x |   |       |       |       |       |       |
yum_utils                            |    |    |    | x | x | x |       |       |       |       |       | Fedora 35
```

Legend:

* empty: don't know/unproven/untested
* "x": proven/works on this OS
* "-": does not currently run on this OS
