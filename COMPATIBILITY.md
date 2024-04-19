# Compatibility

Which Ansible role is proven to run on which OS?

```
                                     |    Debian    |   RHEL    |        Ubuntu         | other
Role                                 | 10 | 11 | 12 | 7 | 8 | 9 | 16.04 | 18.04 | 20.04 |
-------------------------------------+----+----+----+---+---+---+-------+-------+-------+-----------
acme_sh                              |    |    |    |   | x |   |       |       |       |
ansible_init                         |    |    |    |   |   |   |       |       |       | Fedora 35+
apache_httpd                         |    |    |    |   |   |   |       |       |       |
apache_solr                          |    |    |    |   |   |   |       |       |       |
apache_tomcat                        |    |    |    |   |   |   |       |       |       |
apps                                 |    |    |    |   |   |   |       |       |       |
at                                   |    |    |    |   |   |   |       |       |       |
audit                                |    |    |    |   |   |   |       |       |       |
bind                                 |    |    |    |   |   |   |       |       |       |
borg_local                           |    |    |    |   |   |   |       |       |       |
chrony                               |    |    |    |   |   |   |       |       |       |
clamav                               |    |    |    |   |   |   |       |       |       |
cloud_init                           |    |    |    |   |   |   |       |       |       |
cockpit                              |    |    |    |   | x | x |   x   |       |       | Fedora 35
collabora                            |    |    |    |   |   |   |       |       |       |
coturn                               |    |    |    |   |   |   |       |       |       |
crypto_policy                        |    |    |    |   |   |   |       |       |       |
dnf_makecache                        |    |    |    |   |   |   |       |       |       |
dnf_versionlock                      |    |    |    |   |   |   |       |       |       |
docker                               |    |    |    |   |   |   |       |       |       |
duplicity                            |    |    |    |   |   |   |       |       |       |
elasticsearch_oss                    |    |    |    |   |   |   |       |       |       |
example                              |    |    |    |   |   |   |       |       |       |
exoscale_vm                          |    |    |    |   |   |   |       |       |       |
fail2ban                             |    |    |    |   |   |   |       |       |       |
fangfrisch                           |    |    |    |   |   |   |       |       |       |
files                                |    |    |    |   |   |   |       |       |       |
firewall                             |    |    |    |   |   |   |       |       |       |
freeipa_client                       |    |    |    |   |   |   |       |       |       |
freeipa_server                       |    |    |    |   |   |   |       |       |       |
github_project_createrepo            |    |    |    |   |   |   |       |       |       |
gitlab_ce                            |    |    |    |   |   |   |       |       |       |
glances                              |    |    |    |   |   |   |       |       |       |
grafana                              |    |    |    |   |   |   |       |       |       |
grafana_grizzly                      |    |    |    |   |   |   |       |       |       |
grav                                 |    |    |    |   |   |   |       |       |       |
graylog_server                       |    |    |    |   |   |   |       |       |       |
haveged                              |    |    |    |   |   |   |       |       |       |
hetzner_vm                           |    |    |    |   |   |   |       |       |       |
hostname                             |    |    |    |   |   |   |       |       |       |
-------------------------------------+----+----+----+---+---+---+-------+-------+-------+-----------
                                     |    Debian    |   RHEL    |        Ubuntu         | other
Role                                 | 10 | 11 | 12 | 7 | 8 | 9 | 16.04 | 18.04 | 20.04 |
-------------------------------------+----+----+----+---+---+---+-------+-------+-------+-----------
icinga2_agent                        |    |    |    |   |   |   |       |       |       |
icinga2_master                       |    |    |    |   |   |   |       |       |       |
icingadb                             |    |    |    |   |   |   |       |       |       |
icingaweb2                           |    |    |    |   |   |   |       |       |       |
icingaweb2_module_businessprocess    |    |    |    |   |   |   |       |       |       |
icingaweb2_module_company            |    |    |    |   |   |   |       |       |       |
icingaweb2_module_director           |    |    |    |   |   |   |       |       |       |
icingaweb2_module_doc                |    |    |    |   |   |   |       |       |       |
icingaweb2_module_grafana            |    |    |    |   |   |   |       |       |       |
icingaweb2_module_incubator          |    |    |    |   |   |   |       |       |       |
icingaweb2_module_monitoring         |    |    |    |   |   |   |       |       |       |
icingaweb2_module_vspheredb          |    |    |    |   |   |   |       |       |       |
icingaweb2_module_x509               |    |    |    |   |   |   |       |       |       |
influxdb                             |    |    |    |   |   |   |       |       |       |
infomaniak_vm                        |    |    |    |   |   |   |       |       |       |
kdump                                |    |    |    |   |   |   |       |       |       |
keepalived                           |    |    |    |   |   |   |       |       |       |
kernel_settings                      |    |    |    |   |   |   |       |       |       |
keycloak                             |    |    |    |   |   |   |       |       |       |
kvm_host                             |    |    |    |   |   |   |       |       |       |
kvm_vm                               |    |    |    |   |   |   |       |       |       |
libmaxminddb                         |    |    |    |   |   |   |       |       |       |
librenms                             |    |    |    |   |   |   |       |       |       |
libreoffice                          |    |    |    |   |   |   |       |       |       |
login                                |    |    |    |   |   |   |       |       |       |
logrotate                            |    |    |    |   |   |   |       |       |       |
mailto_root                          |    |    |    |   |   |   |       |       |       |
mailx                                |    |    |    |   |   |   |       |       |       |
mariadb_client                       |    |    |    |   |   |   |       |       |       |
mariadb_server                       |    |    |    |   |   |   |       |       |       |
maxmind_geoip                        |    |    |    |   |   |   |       |       |       |
minio_client                         |    |    |    |   |   |   |       |       |       |
mirror                               |    |    |    |   |   |   |       |       |       |
mod_maxminddb                        |    |    |    |   |   |   |       |       |       |
mongodb                              |    |    |    |   |   |   |       |       |       |
monitoring_plugins                   |  x |    |    | x | x |   |   x   |       |       | Debian 9, Fedora, Suse, Windows
monitoring_plugins_grafana_dashboards|    |    |    |   |   |   |       |       |       |
motd                                 |    |    |    |   |   |   |       |       |       |
mount                                |    |    |    |   |   |   |       |       |       |
network                              |    |    |    |   |   |   |       |       |       |
-------------------------------------+----+----+----+---+---+---+-------+-------+-------+-----------
                                     |    Debian    |   RHEL    |        Ubuntu         | other
Role                                 | 10 | 11 | 12 | 7 | 8 | 9 | 16.04 | 18.04 | 20.04 |
-------------------------------------+----+----+----+---+---+---+-------+-------+-------+-----------
nextcloud                            |    |    |    |   |   |   |       |       |       |
nfs_client                           |    |    |    |   |   |   |       |       |       |
nfs_server                           |    |    |    |   |   |   |       |       |       |
nodejs                               |    |    |    |   |   |   |       |       |       |
objectstore_backup                   |    |    |    |   |   |   |       |       |       |
opensearch                           |    |    |    |   |   |   |       |       |       |
openssl                              |    |    |    |   |   |   |       |       |       |
open_vm_tools                        |    |    |    |   |   |   |       |       |       |
openvpn_server                       |    |    |    |   |   |   |       |       |       |
perl                                 |    |    |    |   |   |   |       |       |       |
php                                  |    |    |    |   |   |   |       |       |       |
policycoreutils                      |    |    |    |   |   |   |       |       |       |
postfix                              |    |    |    |   |   |   |       |       |       |
postgresql_server                    |    |    |    |   |   |   |       |       |       |
python                               |    |    |    |   |   |   |       |       |       |
python_venv                          |    |    |    |   |   |   |       |       |       |
qemu_guest_agent                     |    |    |    |   |   |   |       |       |       |
redis                                |    |    |    |   |   |   |       |       |       |
repo_baseos                          |    |    |    |   |   |   |       |       |       |
repo_collabora                       |    |    |    |   |   |   |       |       |       |
repo_collabora_code                  |    |    |    |   |   |   |       |       |       |
repo_debian_base                     |    |    |    |   |   |   |       |       |       |
repo_docker                          |    |    |    |   |   |   |       |       |       |
repo_elasticsearch                   |    |    |    |   |   |   |       |       |       |
repo_elasticsearch_oss               |    |    |    |   |   |   |       |       |       |
repo_epel                            |    |    |    |   |   |   |       |       |       |
repo_gitlab_ce                       |    |    |    |   |   |   |       |       |       |
repo_gitlab_runner                   |    |    |    |   |   |   |       |       |       |
repo_grafana                         |    |    |    |   |   |   |       |       |       |
repo_graylog                         |    |    |    |   |   |   |       |       |       |
repo_icinga                          |    |    |    |   |   |   |       |       |       |
repo_influxdb                        |    |    |    |   |   |   |       |       |       |
repo_mariadb                         |    |    |    |   |   |   |       |       |       |
repo_mongodb                         |    | x  |    |   | x | x |       |       |       |
repo_monitoring_plugins              |    |    |    |   |   |   |       |       |       |
repo_mydumper                        |    |    |    |   |   |   |       |       |       |
repo_opensearch                      |    |    |    |   |   |   |       |       |       |
repo_postgresql                      |    |    |    |   |   |   |       |       |       |
repo_remi                            |    |    |    |   |   |   |       |       |       |
repo_rpmfusion                       |    |    |    |   |   |   |       |       |       |
-------------------------------------+----+----+----+---+---+---+-------+-------+-------+-----------
                                     |    Debian    |   RHEL    |        Ubuntu         | other
Role                                 | 10 | 11 | 12 | 7 | 8 | 9 | 16.04 | 18.04 | 20.04 |
-------------------------------------+----+----+----+---+---+---+-------+-------+-------+-----------
repo_sury                            |    |    |    |   |   |   |       |       |       |
rocketchat                           |    |    |    |   |   |   |       |       |       |
rsyslog                              |    |    |    |   |   |   |       |       |       |
selinux                              |    |    |    |   |   |   |       |       |       |
shared                               |    |    |    |   |   |   |       |       |       |
snmp                                 |    |    |    |   |   |   |       |       |       |
sshd                                 |    |    |    |   |   |   |       |       |       |
systemd_journald                     |    |    |    |   |   |   |       |       |       |
systemd_unit                         |    |    |    |   |   |   |       |       |       |
system_update                        |    |    |    |   |   |   |       |       |       |
tar                                  |    |    |    |   |   |   |       |       |       |
telegraf                             |    |    |    |   |   |   |       |       |       |
timezone                             |    |    |    |   |   |   |       |       |       |
tools                                |    |    |    |   |   |   |       |       |       |
unattended_upgrades                  |    |    |    |   |   |   |       |       |       |
wordpress                            |    |    |    |   |   |   |       |       |       |
yum_utils                            |    |    |    |   |   |   |       |       |       |
```

Legend:

* empty: don't know/unproven/untested
* "x": proven/works on this OS
