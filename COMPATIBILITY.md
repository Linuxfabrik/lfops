# Compatibility

Which Ansible role is proven to run on which OS?

```
                                     |  Debian |  RHEL |         Ubuntu        | other
Role                                 | 11 | 12 | 8 | 9 | 20.04 | 22.04 | 24.04 |
-------------------------------------+----+----+---+---+-------+-------+-------+-----------
acme_sh                              |    |    | x | x |       |       |       |
ansible_init                         |    |    |   |   |       |       |       | Fedora 35+
apache_httpd                         |    | x  | x | x |       |       |       |
apache_solr                          |    |    | x | x |       |       |       |
apache_tomcat                        |    |    | x |   |       |       |       |
apps                                 |    |    | x | x |       |       |       |
at                                   |    |    | x | x |       |       |       | Fedora 35
audit                                |    |    | x | x |       |       |       |
bind                                 |    |    | x | x |       |       |       |
borg_local                           |    |    | x |   |       |       |       |
chrony                               |    |    | x | x |       |       |       |
clamav                               |    |    | x |   |       |       |       |
cloud_init                           |    |    | x | x |       |       |       |
cockpit                              |    |    | x | x |       |       |       | Fedora 35
collabora                            |    |    | x |   |       |       |       |
collect_rpmnew_rpmsave               |    |    | x | x |       |       |       | Fedora 40
coturn                               |    |    | x |   |       |       |       |
crypto_policy                        |    |    | x | x |       |       |       |
dnf_makecache                        |    |    | x | x |       |       |       |
dnf_versionlock                      |    |    | x |   |       |       |       |
docker                               |    |    | x |   |       |       |       |
duplicity                            |    |    | x | x |       |       |       | Fedora 35
elasticsearch_oss                    |    |    | x |   |       |       |       |
exoscale_vm                          |    |    |   |   |       |       |       | Fedora 35+
fail2ban                             |    |    | x | x |       |       |       |
fangfrisch                           |    |    | x |   |       |       |       |
files                                |    |    | x | x |       |       |       |
firewall                             |    |    | x | x |       |       |       |
freeipa_client                       |    |    | x | x |       |       |       |
freeipa_server                       |    |    | x | x |       |       |       |
github_project_createrepo            |    |    | x |   |       |       |       |
gitlab_ce                            |    |    | x |   |       |       |       |
glances                              |    |    | x | x |       |       |       |
grafana                              |    |    | x | x |       |       |       |
grafana_grizzly                      |    |    | x | x |       |       |       |
grav                                 |    |    | x |   |       |       |       |
graylog_server                       | x  |    | x |   |       |       |       |
haveged                              |    |    | x | x |       |       |       |
hetzner_vm                           |    |    |   |   |       |       |       | Fedora 35+
hostname                             |    |    | x | x |       |       |       |
-------------------------------------+----+----+---+---+-------+-------+-------+-----------
                                     |  Debian |  RHEL |         Ubuntu        | other
Role                                 | 11 | 12 | 8 | 9 | 20.04 | 22.04 | 24.04 |
-------------------------------------+----+----+---+---+-------+-------+-------+-----------
icinga2_agent                        |    |    | x | x |       |       |       | Fedora 35
icinga2_master                       |    |    | x | x |       |       |       |
icingadb                             |    | x  | x | x |       |       |       |
icingadb_web                         |    | x  | x | x |       |       |       |
icingaweb2                           |    | x  | x | x |       |       |       |
icingaweb2_module_businessprocess    |    | x  | x | x |       |       |       |
icingaweb2_module_company            |    | x  | x | x |       |       |       |
icingaweb2_module_director           |    | x  | x | x |       |       |       |
icingaweb2_module_doc                |    |    | x | x |       |       |       |
icingaweb2_module_grafana            |    | x  | x | x |       |       |       |
icingaweb2_module_incubator          |    | x  | x | x |       |       |       |
icingaweb2_module_monitoring         |    | x  | x | x |       |       |       |
icingaweb2_module_vspheredb          |    | x  | x | x |       |       |       |
icingaweb2_module_x509               |    | x  | x | x |       |       |       |
influxdb                             |    | x  | x | x |       |       |       |
infomaniak_vm                        |    |    |   |   |       |       |       | Fedora 35+
kdump                                |    |    | x | x |       |       |       |
keepalived                           |    |    | x |   |       |       |       |
kernel_settings                      | -  | -  | x | x |   -   |       |       |
keycloak                             |    |    | x |   |       |       |       |
kvm_host                             |    |    | x |   |       |       |       |
kvm_vm                               |    |    | x |   |       |       |       |
libmaxminddb                         |    |    | x |   |       |       |       |
librenms                             |    |    | x |   |       |       |       |
libreoffice                          |    |    | x |   |       |       |       |
login                                |    |    | x | x |       |       |       | Fedora 35+
logrotate                            |    |    | x | x |       |       |       | Fedora
mailto_root                          |    |    | x | x |       |       |       |
mailx                                | x  | x  | x | x |       |       |       | Fedora
mariadb_server                       | -  | -  | x | x |   -   |       |       |
maxmind_geoip                        |    |    | x |   |       |       |       |
minio_client                         |    |    | x |   |       |       |       |
mirror                               |    |    | x | x |       |       |       |
mod_maxminddb                        |    |    | x |   |       |       |       |
mongodb                              | x  |    | x | x |       |       |       |
monitoring_plugins                   |    |    | x | x |       |       |       | Debian 9, Fedora, Suse, Windows
monitoring_plugins_grafana_dashboards|    |    | x | x |       |       |       |
motd                                 |    |    | x | x |       |       |       |
mount                                | x  |    | x | x |       |       |       |
network                              |    |    | x | x |       |       |       |
-------------------------------------+----+----+---+---+-------+-------+-------+-----------
                                     |  Debian |  RHEL |         Ubuntu        | other
Role                                 | 11 | 12 | 8 | 9 | 20.04 | 22.04 | 24.04 |
-------------------------------------+----+----+---+---+-------+-------+-------+-----------
nextcloud                            |    |    | x |   |       |       |       |
nfs_client                           | x  |    | x | x |       |       |       |
nfs_server                           | x  |    | x |   |       |       |       |
nodejs                               |    |    | x | x |       |       |       |
objectstore_backup                   |    |    | x |   |       |       |       |
opensearch                           | x  |    | x |   |       |       |       |
open_vm_tools                        |    |    | x | x |       |       |       |
openvpn_server                       |    |    | x | x |       |       |       |
php                                  |    | x  | x | x |       |       |       |
policycoreutils                      |    |    | x | x |       |       |       | Fedora 35
postfix                              | x  | x  | x | x |       |       |       | Fedora 35
postgresql_server                    |    |    | x |   |       |       |       |
python                               |    | x  | x | x |       |       |       | Windows
python_venv                          | x  | x  | x | x |       |       |       | Fedora 35
qemu_guest_agent                     |    |    | x | x |       |       |       |
redis                                |    | x  | x | x |       |       |       |
repo_baseos                          |    |    | x | x |       |       |       |
repo_collabora                       |    |    | x |   |       |       |       |
repo_collabora_code                  |    |    | x |   |       |       |       |
repo_debian_base                     | x  |    |   |   |       |       |       |
repo_docker                          |    |    | x |   |       |       |       |
repo_elasticsearch                   |    |    | x |   |       |       |       |
repo_elasticsearch_oss               |    |    | x |   |       |       |       |
repo_epel                            |    |    | x | x |       |       |       |
repo_gitlab_ce                       |    |    | x |   |       |       |       |
repo_gitlab_runner                   |    |    | x |   |       |       |       |
repo_grafana                         |    | x  | x | x |       |       |       |
repo_graylog                         | x  |    | x |   |       |       |       |
repo_icinga                          |    | x  | x | x |       |       |       |
repo_influxdb                        | x  | x  | x | x |       |       |       |
repo_mariadb                         |    |    | x | x |       |       |       |
repo_mongodb                         | x  |    | x | x |       |       |       |
repo_monitoring_plugins              | x  |    | x | x |   x   |   x   |       |
repo_mydumper                        |    |    | x | x |       |       |       |
repo_opensearch                      | x  |    | x |   |       |       |       |
repo_postgresql                      |    |    | x |   |       |       |       |
repo_redis                           |    | x  |   |   |       |       |       |
repo_remi                            |    |    | x | x |       |       |       | Fedora 35
-------------------------------------+----+----+---+---+-------+-------+-------+-----------
                                     |  Debian |  RHEL |         Ubuntu        | other
Role                                 | 11 | 12 | 8 | 9 | 20.04 | 22.04 | 24.04 |
-------------------------------------+----+----+---+---+-------+-------+-------+-----------
repo_rpmfusion                       |    |    | x |   |       |       |       |
repo_sury                            | x  | x  | - | - |       |       |       |
rocketchat                           |    |    | x |   |       |       |       | Fedora 35
rsyslog                              |    |    | x | x |       |       |       |
selinux                              |    |    | x | x |       |       |       |
snmp                                 |    |    | x | x |       |       |       |
sshd                                 |    |    | x | x |       |       |       |
system_update                        | x  | x  | x | x |       |       |       |
systemd_journald                     |    |    | x | x |       |       |       |
systemd_unit                         |    |    | x | x |       |       |       |
telegraf                             |    |    | x |   |       |       |       |
timezone                             |    |    | x | x |       |       |       | Fedora 35
tools                                |    |    | x | x |       |       |       | Fedora
unattended_upgrades                  | x  |    |   |   |       |       |       |
vsftpd                               |    |    | x |   |       |       |       |
wordpress                            |    |    | x |   |       |       |       |
yum_utils                            |    |    | x | x |       |       |       | Fedora 35
```

Legend:

* empty: don't know/unproven/untested
* "x": proven/works on this OS
* "-": does not currently run on this OS
