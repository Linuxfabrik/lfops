# Compatibility

Which Ansible role is proven to run on which OS?

| Role                                  | Deb 12 | Deb 13 | RHEL 8 | RHEL 9 | RHEL 10 | Ubu 22.04 | Ubu 24.04 | Ubu 26.04 | Other                                        |
|---------------------------------------|:------:|:------:|:------:|:------:|:-------:|:---------:|:---------:|:---------:|----------------------------------------------|
| acme_sh                               |   x    |   x    |   x    |   x    |    x    |    (x)    |     x     |    (x)    |                                              |
| alternatives                          |   x    |   x    |   x    |   x    |   (x)   |     x     |     x     |    (x)    |                                              |
| ansible_init                          |        |        |        |        |         |           |           |           | Fedora 35+                                   |
| apache_httpd                          |   x    |   x    |   x    |   x    |    x    |    (x)    |     x     |    (x)    |                                              |
| apache_solr                           |        |        |   x    |   x    |   (x)   |           |           |           |                                              |
| apache_tomcat                         |        |        |   x    |   x    |   (x)   |           |           |           |                                              |
| apps                                  |  (x)   |  (x)   |   x    |   x    |    x    |    (x)    |    (x)    |    (x)    |                                              |
| at                                    |  (x)   |  (x)   |   x    |   x    |    x    |    (x)    |    (x)    |    (x)    | Fedora 35                                    |
| audit                                 |        |        |   x    |   x    |   (x)   |           |           |           |                                              |
| bind                                  |        |        |   x    |   x    |    x    |           |           |           |                                              |
| blocky                                |        |        |   x    |   x    |   (x)   |           |           |           |                                              |
| borg_local                            |        |        |   x    |  (x)   |   (x)   |           |           |           |                                              |
| chrony                                |        |        |   x    |   x    |    x    |           |           |           |                                              |
| clamav                                |        |        |   x    |   x    |   (x)   |           |           |           |                                              |
| cloud_init                            |  (x)   |  (x)   |   x    |   x    |    x    |    (x)    |    (x)    |    (x)    |                                              |
| cockpit                               |        |        |   x    |   x    |    x    |           |           |           | Fedora 35                                    |
| collabora                             |        |        |   x    |   x    |   (x)   |           |           |           |                                              |
| collect_rpmnew_rpmsave                |  (x)   |  (x)   |   x    |   x    |   (x)   |    (x)    |    (x)    |    (x)    | Fedora 40                                    |
| coturn                                |        |        |   x    |   x    |   (x)   |           |           |           |                                              |
| crypto_policy                         |        |        |   x    |   x    |    x    |           |           |           |                                              |
| dnf_makecache                         |        |        |   x    |   x    |    x    |           |           |           |                                              |
| dnf_versionlock                       |        |        |   x    |   x    |         |           |           |           | Fedora 40                                    |
| docker                                |        |        |   x    |  (x)   |   (x)   |           |           |           |                                              |
| duplicity                             |        |        |   x    |   x    |    x    |           |           |           | Fedora 35                                    |
| elastic_agent                         |  (x)   |  (x)   |  (x)   |   x    |   (x)   |    (x)    |     x     |    (x)    |                                              |
| elastic_agent_fleet_server            |  (x)   |  (x)   |  (x)   |   x    |   (x)   |    (x)    |     x     |    (x)    |                                              |
| elasticsearch                         |  (x)   |  (x)   |   x    |   x    |   (x)   |    (x)    |     x     |    (x)    |                                              |
| exoscale_vm                           |        |        |        |        |         |           |           |           | Fedora 35+                                   |
| fail2ban                              |        |        |   x    |   x    |   (x)   |           |           |           |                                              |
| fangfrisch                            |        |        |  (x)   |   x    |   (x)   |           |           |           |                                              |
| files                                 |  (x)   |  (x)   |   x    |   x    |    x    |    (x)    |    (x)    |    (x)    |                                              |
| firewall                              |   x    |   x    |   x    |   x    |    x    |     x     |     x     |    (x)    |                                              |
| freeipa_client                        |        |        |   x    |   x    |    x    |           |           |           |                                              |
| freeipa_server                        |        |        |   x    |   x    |    x    |           |           |           |                                              |
| github_project_createrepo             |        |        |   x    |  (x)   |   (x)   |           |           |           |                                              |
| gitlab_ce                             |        |        |   x    |  (x)   |   (x)   |           |           |           |                                              |
| glances                               |  (x)   |  (x)   |   x    |   x    |   (x)   |    (x)    |    (x)    |    (x)    |                                              |
| glpi_agent                            |        |        |   x    |   x    |   (x)   |           |           |           |                                              |
| grafana                               |        |        |   x    |   x    |    x    |           |           |           |                                              |
| grafana_grizzly                       |  (x)   |  (x)   |   x    |   x    |   (x)   |    (x)    |    (x)    |    (x)    |                                              |
| grav                                  |        |        |   x    |  (x)   |   (x)   |           |           |           |                                              |
| graylog_datanode                      |   x    |   x    |   x    |   x    |   (x)   |    (x)    |    (x)    |    (x)    |                                              |
| graylog_server                        |   x    |   x    |   x    |  (x)   |   (x)   |    (x)    |    (x)    |    (x)    |                                              |
| haveged                               |  (x)   |  (x)   |   x    |   x    |   (x)   |    (x)    |    (x)    |    (x)    |                                              |
| hetzner_vm                            |        |        |        |        |         |           |           |           | Fedora 35+                                   |
| hostname                              |  (x)   |  (x)   |   x    |   x    |    x    |    (x)    |    (x)    |    (x)    |                                              |
| icinga2_agent                         |  (x)   |   x    |   x    |   x    |    x    |    (x)    |    (x)    |    (x)    | Fedora 35                                    |
| icinga2_master                        |   x    |   x    |   x    |   x    |   (x)   |    (x)    |    (x)    |    (x)    |                                              |
| icinga_kubernetes                     |        |        |  (x)   |   x    |   (x)   |           |           |           |                                              |
| icinga_kubernetes_web                 |  (x)   |  (x)   |  (x)   |   x    |   (x)   |    (x)    |    (x)    |    (x)    |                                              |
| icingadb                              |   x    |   x    |   x    |   x    |   (x)   |    (x)    |    (x)    |    (x)    |                                              |
| icingadb_web                          |   x    |   x    |   x    |   x    |   (x)   |    (x)    |    (x)    |    (x)    |                                              |
| icingaweb2                            |   x    |   x    |   x    |   x    |   (x)   |    (x)    |    (x)    |    (x)    |                                              |
| icingaweb2_module_businessprocess     |   x    |   x    |   x    |   x    |   (x)   |    (x)    |    (x)    |    (x)    |                                              |
| icingaweb2_module_company             |   x    |   x    |   x    |   x    |   (x)   |    (x)    |    (x)    |    (x)    |                                              |
| icingaweb2_module_cube                |   x    |   x    |   x    |   x    |   (x)   |    (x)    |    (x)    |    (x)    |                                              |
| icingaweb2_module_director            |   x    |   x    |   x    |   x    |   (x)   |    (x)    |    (x)    |    (x)    |                                              |
| icingaweb2_module_doc                 |   x    |   x    |   x    |   x    |   (x)   |    (x)    |    (x)    |    (x)    |                                              |
| icingaweb2_module_fileshipper         |   x    |   x    |   x    |   x    |   (x)   |    (x)    |    (x)    |    (x)    |                                              |
| icingaweb2_module_generictts          |   x    |   x    |   x    |   x    |   (x)   |    (x)    |    (x)    |    (x)    |                                              |
| icingaweb2_module_grafana             |   x    |   x    |   x    |   x    |   (x)   |    (x)    |    (x)    |    (x)    |                                              |
| icingaweb2_module_incubator           |   x    |   x    |   x    |   x    |   (x)   |    (x)    |    (x)    |    (x)    |                                              |
| icingaweb2_module_jira                |  (x)   |  (x)   |   x    |   x    |   (x)   |    (x)    |    (x)    |    (x)    |                                              |
| icingaweb2_module_pdfexport           |   x    |   x    |   x    |   x    |   (x)   |    (x)    |    (x)    |    (x)    |                                              |
| icingaweb2_module_reporting           |  (x)   |  (x)   |   x    |  (x)   |   (x)   |    (x)    |    (x)    |    (x)    |                                              |
| icingaweb2_module_vspheredb           |   x    |   x    |   x    |   x    |   (x)   |    (x)    |    (x)    |    (x)    |                                              |
| icingaweb2_module_x509                |   x    |   x    |   x    |   x    |   (x)   |    (x)    |    (x)    |    (x)    |                                              |
| icingaweb2_theme_linuxfabrik          |  (x)   |  (x)   |   x    |   x    |   (x)   |    (x)    |     x     |    (x)    |                                              |
| influxdb                              |   x    |   x    |   x    |   x    |   (x)   |    (x)    |    (x)    |    (x)    |                                              |
| infomaniak_vm                         |        |        |        |        |         |           |           |           | Fedora 35+                                   |
| kdump                                 |        |        |   x    |   x    |    x    |           |           |           |                                              |
| keepalived                            |        |        |   x    |  (x)   |   (x)   |           |           |           |                                              |
| kernel_settings                       |   x    |   x    |   x    |   x    |   (x)   |    (x)    |    (x)    |    (x)    |                                              |
| keycloak                              |        |        |   x    |  (x)   |   (x)   |           |           |           |                                              |
| kibana                                |  (x)   |  (x)   |  (x)   |   x    |   (x)   |    (x)    |     x     |    (x)    |                                              |
| kvm_host                              |  (x)   |  (x)   |   x    |  (x)   |   (x)   |    (x)    |     x     |    (x)    |                                              |
| kvm_vm                                |  (x)   |  (x)   |   x    |  (x)   |   (x)   |    (x)    |     x     |    (x)    |                                              |
| libmaxminddb                          |  (x)   |  (x)   |   x    |  (x)   |   (x)   |    (x)    |    (x)    |    (x)    |                                              |
| librenms                              |        |        |   x    |  (x)   |   (x)   |           |           |           |                                              |
| libreoffice                           |        |        |   x    |  (x)   |   (x)   |           |           |           |                                              |
| login                                 |  (x)   |  (x)   |   x    |   x    |    x    |    (x)    |    (x)    |    (x)    | Fedora 35+                                   |
| logrotate                             |  (x)   |  (x)   |   x    |   x    |    x    |    (x)    |    (x)    |    (x)    | Fedora                                       |
| logstash                              |  (x)   |  (x)   |  (x)   |   x    |   (x)   |    (x)    |     x     |    (x)    |                                              |
| lvm                                   |        |        |  (x)   |  (x)   |    x    |           |           |           |                                              |
| mailto_root                           |  (x)   |  (x)   |   x    |   x    |    x    |    (x)    |    (x)    |    (x)    |                                              |
| mailx                                 |   x    |   x    |   x    |   x    |    x    |    (x)    |    (x)    |    (x)    | Fedora                                       |
| mariadb_server                        |   x    |   x    |   x    |   x    |    x    |    (x)    |    (x)    |    (x)    | Galera on Debian is untested                 |
| mastodon                              |  (x)   |  (x)   |  (x)   |   x    |   (x)   |    (x)    |    (x)    |    (x)    |                                              |
| maxmind_geoip                         |  (x)   |  (x)   |   x    |  (x)   |   (x)   |    (x)    |    (x)    |    (x)    |                                              |
| mirror                                |        |        |   x    |   x    |   (x)   |           |           |           |                                              |
| mod_maxminddb                         |  (x)   |  (x)   |   x    |  (x)   |   (x)   |    (x)    |    (x)    |    (x)    |                                              |
| mongodb                               |   x    |   x    |   x    |   x    |   (x)   |    (x)    |    (x)    |    (x)    |                                              |
| monitoring_plugins                    |  (x)   |  (x)   |   x    |   x    |    x    |    (x)    |    (x)    |    (x)    | Debian 9, Fedora, SLES 15, SLES 16, Windows  |
| monitoring_plugins_grafana_dashboards |  (x)   |  (x)   |   x    |   x    |   (x)   |    (x)    |    (x)    |    (x)    |                                              |
| moodle                                |   -    |   -    |   x    |   x    |   (x)   |           |           |           |                                              |
| motd                                  |  (x)   |  (x)   |   x    |   x    |    x    |    (x)    |    (x)    |    (x)    |                                              |
| mount                                 |  (x)   |  (x)   |   x    |   x    |   (x)   |    (x)    |    (x)    |    (x)    |                                              |
| network                               |   -    |   -    |   x    |   x    |    x    |           |           |           |                                              |
| nextcloud                             |        |        |   x    |   x    |   (x)   |           |           |           |                                              |
| nfs_client                            |  (x)   |  (x)   |   x    |   x    |   (x)   |    (x)    |    (x)    |    (x)    |                                              |
| nfs_server                            |  (x)   |  (x)   |   x    |  (x)   |   (x)   |    (x)    |    (x)    |    (x)    |                                              |
| nodejs                                |  (x)   |  (x)   |   x    |   x    |   (x)   |    (x)    |    (x)    |    (x)    |                                              |
| open_vm_tools                         |        |        |   x    |   x    |   (x)   |           |           |           |                                              |
| opensearch                            |        |        |   x    |  (x)   |   (x)   |           |           |           |                                              |
| openvpn_server                        |        |        |   x    |   x    |    x    |           |           |           |                                              |
| php                                   |   x    |   x    |   x    |   x    |   (x)   |    (x)    |    (x)    |    (x)    |                                              |
| podman_containers                     |        |        |  (x)   |   x    |   (x)   |           |           |           |                                              |
| policycoreutils                       |        |        |   x    |   x    |    x    |           |           |           | Fedora 35                                    |
| postfix                               |   x    |   x    |   x    |   x    |    x    |    (x)    |    (x)    |    (x)    | Fedora 35                                    |
| postgresql_server                     |        |        |   x    |  (x)   |   (x)   |           |           |           |                                              |
| proxysql                              |        |        |   x    |  (x)   |   (x)   |           |           |           |                                              |
| python                                |   x    |   x    |   x    |   x    |    x    |    (x)    |    (x)    |    (x)    | Windows                                      |
| python_venv                           |   x    |   x    |   x    |   x    |    x    |    (x)    |    (x)    |    (x)    | Fedora 35                                    |
| qemu_guest_agent                      |  (x)   |  (x)   |   x    |   x    |    x    |    (x)    |    (x)    |    (x)    |                                              |
| redis                                 |   x    |   x    |   x    |   x    |   (x)   |    (x)    |    (x)    |    (x)    |                                              |
| repo_baseos                           |        |        |   x    |   x    |    x    |           |           |           |                                              |
| repo_collabora                        |        |        |   x    |  (x)   |   (x)   |           |           |           |                                              |
| repo_collabora_code                   |        |        |   x    |   x    |   (x)   |           |           |           |                                              |
| repo_debian_base                      |  (x)   |  (x)   |   -    |   -    |         |    (x)    |    (x)    |    (x)    |                                              |
| repo_docker                           |        |        |   x    |  (x)   |   (x)   |           |           |           |                                              |
| repo_elasticsearch                    |  (x)   |  (x)   |   x    |   x    |   (x)   |    (x)    |     x     |    (x)    |                                              |
| repo_epel                             |        |        |   x    |   x    |    x    |           |           |           |                                              |
| repo_gitlab_ce                        |        |        |   x    |  (x)   |   (x)   |           |           |           |                                              |
| repo_gitlab_runner                    |        |        |   x    |  (x)   |   (x)   |           |           |           |                                              |
| repo_google_chrome                    |        |        |   x    |   x    |   (x)   |           |           |           |                                              |
| repo_grafana                          |   x    |   x    |   x    |   x    |   (x)   |    (x)    |    (x)    |    (x)    |                                              |
| repo_graylog                          |   x    |   x    |   x    |  (x)   |   (x)   |    (x)    |    (x)    |    (x)    |                                              |
| repo_icinga                           |   x    |   x    |   x    |   x    |    x    |     x     |    (x)    |    (x)    |                                              |
| repo_influxdb                         |   x    |   x    |   x    |   x    |   (x)   |    (x)    |    (x)    |    (x)    |                                              |
| repo_mariadb                          |   x    |   x    |   x    |   x    |    x    |    (x)    |     x     |    (x)    |                                              |
| repo_mongodb                          |   x    |   x    |   x    |   x    |   (x)   |    (x)    |    (x)    |    (x)    |                                              |
| repo_monitoring_plugins               |  (x)   |  (x)   |   x    |   x    |    x    |     x     |    (x)    |    (x)    | SLES 15, SLES 16                             |
| repo_mydumper                         |  (x)   |  (x)   |   x    |   x    |   (x)   |    (x)    |    (x)    |    (x)    |                                              |
| repo_opensearch                       |   x    |   x    |   x    |  (x)   |   (x)   |     x     |     x     |    (x)    |                                              |
| repo_postgresql                       |        |        |  (x)   |   x    |   (x)   |           |           |           |                                              |
| repo_proxysql                         |  (x)   |  (x)   |   x    |   x    |   (x)   |    (x)    |    (x)    |    (x)    |                                              |
| repo_redis                            |   x    |   x    |        |        |         |    (x)    |    (x)    |    (x)    |                                              |
| repo_remi                             |        |        |   x    |   x    |    x    |           |           |           |                                              |
| repo_rpmfusion                        |        |        |   x    |  (x)   |   (x)   |           |           |           |                                              |
| repo_sury                             |   x    |   x    |   -    |   -    |         |    (x)    |    (x)    |    (x)    |                                              |
| rocketchat                            |        |        |   x    |  (x)   |   (x)   |           |           |           | Fedora 35                                    |
| rsyslog                               |        |        |   x    |   x    |    x    |           |           |           |                                              |
| selinux                               |  (x)   |  (x)   |   x    |   x    |    x    |    (x)    |    (x)    |    (x)    |                                              |
| shared                                |        |        |        |        |         |           |           |           | controller-side helper, target OS irrelevant |
| shell                                 |  (x)   |  (x)   |   x    |   x    |    x    |    (x)    |    (x)    |    (x)    |                                              |
| snmp                                  |        |        |   x    |   x    |   (x)   |           |           |           |                                              |
| squid                                 |        |        |  (x)   |   x    |   (x)   |           |           |           |                                              |
| sshd                                  |   x    |   x    |   x    |   x    |    x    |    (x)    |    (x)    |    (x)    | Fedora 40                                    |
| system_update                         |   x    |   x    |   x    |   x    |    x    |    (x)    |    (x)    |    (x)    |                                              |
| systemd_journald                      |        |        |   x    |   x    |    x    |           |           |           |                                              |
| systemd_unit                          |        |        |   x    |   x    |    x    |           |           |           |                                              |
| telegraf                              |        |        |   x    |  (x)   |   (x)   |           |           |           |                                              |
| timezone                              |  (x)   |  (x)   |   x    |   x    |    x    |    (x)    |    (x)    |    (x)    | Fedora 35                                    |
| tools                                 |        |        |   x    |   x    |    x    |           |           |           | Fedora                                       |
| unattended_upgrades                   |  (x)   |  (x)   |        |        |         |    (x)    |    (x)    |    (x)    |                                              |
| uptimerobot                           |        |        |        |        |         |           |           |           | controller-side, talks to UptimeRobot API    |
| vsftpd                                |        |        |   x    |  (x)   |   (x)   |           |           |           |                                              |
| wordpress                             |        |        |   x    |  (x)   |   (x)   |           |           |           |                                              |
| yum_utils                             |        |        |   x    |   x    |    x    |           |           |           | Fedora 35                                    |

Legend:

* `Deb` = Debian, `Ubu` = Ubuntu.
* empty: don't know / unproven / untested
* `x`: proven / works on this OS
* `(x)`: theoretically usable but untested (inferred from role code)
* `-`: does not currently run on this OS
