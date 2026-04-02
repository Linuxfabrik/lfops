# Playbooks

This document lists all playbooks and the roles they call. Skip variables allow you to disable specific roles or dependencies within a playbook. Set them to `true` in your inventory to skip the corresponding role.

All skip variables are booleans and default to `false` unless noted otherwise.

For playbooks with role injections (typically `setup_*` playbooks), two types of skip variables are available:

* `playbook__role__skip_role`: Skips the role entirely and disables its injections into other roles.
* `playbook__role__skip_injections`: Only disables the injections, the role itself still runs.

See the [main README](../README.md#skipping-roles-in-a-playbook) for details.


## acme_sh.yml

Calls the following roles (in order):

* [apps](https://github.com/Linuxfabrik/lfops/tree/main/roles/apps)
* [acme_sh](https://github.com/Linuxfabrik/lfops/tree/main/roles/acme_sh)


## alternatives.yml

Calls the following roles (in order):

* [alternatives](https://github.com/Linuxfabrik/lfops/tree/main/roles/alternatives)


## ansible_init.yml

Calls the following roles (in order):

* [ansible_init](https://github.com/Linuxfabrik/lfops/tree/main/roles/ansible_init)


## apache_httpd.yml

Calls the following roles (in order):

* [repo_baseos](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_baseos): `apache_httpd__skip_repo_baseos`
* [repo_epel](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_epel): `apache_httpd__skip_repo_epel`
* [policycoreutils](https://github.com/Linuxfabrik/lfops/tree/main/roles/policycoreutils): `apache_httpd__skip_policycoreutils`
* [selinux](https://github.com/Linuxfabrik/lfops/tree/main/roles/selinux): `apache_httpd__skip_selinux`
* [python](https://github.com/Linuxfabrik/lfops/tree/main/roles/python): `apache_httpd__skip_python`
* [apache_httpd](https://github.com/Linuxfabrik/lfops/tree/main/roles/apache_httpd)


## apache_solr.yml

Calls the following roles (in order):

* [apps](https://github.com/Linuxfabrik/lfops/tree/main/roles/apps)
* [apache_solr](https://github.com/Linuxfabrik/lfops/tree/main/roles/apache_solr)


## apache_tomcat.yml

Calls the following roles (in order):

* [repo_baseos](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_baseos): `apache_tomcat__skip_repo_baseos`
* [repo_epel](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_epel)
* [policycoreutils](https://github.com/Linuxfabrik/lfops/tree/main/roles/policycoreutils)
* [apache_tomcat](https://github.com/Linuxfabrik/lfops/tree/main/roles/apache_tomcat)


## apps.yml

Calls the following roles (in order):

* [apps](https://github.com/Linuxfabrik/lfops/tree/main/roles/apps)


## at.yml

Calls the following roles (in order):

* [at](https://github.com/Linuxfabrik/lfops/tree/main/roles/at)


## audit.yml

Calls the following roles (in order):

* [audit](https://github.com/Linuxfabrik/lfops/tree/main/roles/audit)


## bind.yml

Calls the following roles (in order):

* [bind](https://github.com/Linuxfabrik/lfops/tree/main/roles/bind)


## blocky.yml

Calls the following roles (in order):

* [blocky](https://github.com/Linuxfabrik/lfops/tree/main/roles/blocky)


## borg_local.yml

Calls the following roles (in order):

* [repo_baseos](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_baseos): `borg_local__skip_repo_baseos`
* [systemd_unit](https://github.com/Linuxfabrik/lfops/tree/main/roles/systemd_unit): `borg_local__skip_systemd_unit`
* [repo_epel](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_epel): `borg_local__skip_repo_epel`
* [borg_local](https://github.com/Linuxfabrik/lfops/tree/main/roles/borg_local)


## chrony.yml

Calls the following roles (in order):

* [chrony](https://github.com/Linuxfabrik/lfops/tree/main/roles/chrony)


## clamav.yml

Calls the following roles (in order):

* [repo_baseos](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_baseos): `clamav__skip_repo_baseos`
* [repo_epel](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_epel): `clamav__skip_repo_epel`
* [policycoreutils](https://github.com/Linuxfabrik/lfops/tree/main/roles/policycoreutils): `clamav__skip_policycoreutils`
* [selinux](https://github.com/Linuxfabrik/lfops/tree/main/roles/selinux): `clamav__skip_selinux`
* [python_venv](https://github.com/Linuxfabrik/lfops/tree/main/roles/python_venv): `clamav__skip_python_venv`
* [clamav](https://github.com/Linuxfabrik/lfops/tree/main/roles/clamav)
* [fangfrisch](https://github.com/Linuxfabrik/lfops/tree/main/roles/fangfrisch): `clamav__skip_fangfrisch`


## cloud_init.yml

Calls the following roles (in order):

* [cloud_init](https://github.com/Linuxfabrik/lfops/tree/main/roles/cloud_init)


## cockpit.yml

Calls the following roles (in order):

* [cockpit](https://github.com/Linuxfabrik/lfops/tree/main/roles/cockpit)


## collabora.yml

Calls the following roles (in order):

* [repo_collabora_code](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_collabora_code): `collabora__skip_repo_collabora_code`
* [repo_collabora](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_collabora): `collabora__skip_repo_collabora` (default: `true`), `collabora__skip_repo_collabora_code`
* [collabora](https://github.com/Linuxfabrik/lfops/tree/main/roles/collabora)


## collect_rpmnew_rpmsave.yml

Calls the following roles (in order):

* [collect_rpmnew_rpmsave](https://github.com/Linuxfabrik/lfops/tree/main/roles/collect_rpmnew_rpmsave)


## coturn.yml

Calls the following roles (in order):

* [repo_baseos](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_baseos): `coturn__skip_repo_baseos`
* [repo_epel](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_epel): `coturn__skip_repo_epel`
* [coturn](https://github.com/Linuxfabrik/lfops/tree/main/roles/coturn)


## crypto_policy.yml

Calls the following roles (in order):

* [crypto_policy](https://github.com/Linuxfabrik/lfops/tree/main/roles/crypto_policy)


## dnf_makecache.yml

Calls the following roles (in order):

* [dnf_makecache](https://github.com/Linuxfabrik/lfops/tree/main/roles/dnf_makecache)


## dnf_versionlock.yml

Calls the following roles (in order):

* [dnf_versionlock](https://github.com/Linuxfabrik/lfops/tree/main/roles/dnf_versionlock)


## docker.yml

Calls the following roles (in order):

* [repo_docker](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_docker): `docker__skip_repo_docker`
* [docker](https://github.com/Linuxfabrik/lfops/tree/main/roles/docker)
* [kernel_settings](https://github.com/Linuxfabrik/lfops/tree/main/roles/kernel_settings): `docker__skip_kernel_settings`


## duplicity.yml

Calls the following roles (in order):

* [repo_baseos](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_baseos): `duplicity__skip_repo_baseos`
* [repo_epel](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_epel)
* [python_venv](https://github.com/Linuxfabrik/lfops/tree/main/roles/python_venv): `duplicity__skip_python_venv`
* [haveged](https://github.com/Linuxfabrik/lfops/tree/main/roles/haveged): `duplicity__skip_haveged`
* [duplicity](https://github.com/Linuxfabrik/lfops/tree/main/roles/duplicity)


## elastic_agent.yml

Calls the following roles (in order):

* [repo_elasticsearch](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_elasticsearch): `elastic_agent__skip_repo_elasticsearch`
* [elastic_agent](https://github.com/Linuxfabrik/lfops/tree/main/roles/elastic_agent)


## elastic_agent_fleet_server.yml

Calls the following roles (in order):

* [repo_elasticsearch](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_elasticsearch): `elastic_agent_fleet_server__skip_repo_elasticsearch`
* [elastic_agent_fleet_server](https://github.com/Linuxfabrik/lfops/tree/main/roles/elastic_agent_fleet_server)


## elasticsearch.yml

Calls the following roles (in order):

* [kernel_settings](https://github.com/Linuxfabrik/lfops/tree/main/roles/kernel_settings): `elasticsearch__skip_kernel_settings`
* [repo_elasticsearch](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_elasticsearch): `elasticsearch__skip_repo_elasticsearch`
* [elasticsearch](https://github.com/Linuxfabrik/lfops/tree/main/roles/elasticsearch)


## exoscale_vm.yml

Calls the following roles (in order):

* [exoscale_vm](https://github.com/Linuxfabrik/lfops/tree/main/roles/exoscale_vm)


## fail2ban.yml

Calls the following roles (in order):

* [repo_baseos](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_baseos): `fail2ban__skip_repo_baseos`
* [policycoreutils](https://github.com/Linuxfabrik/lfops/tree/main/roles/policycoreutils)
* [selinux](https://github.com/Linuxfabrik/lfops/tree/main/roles/selinux): `fail2ban__skip_selinux`
* [sshd](https://github.com/Linuxfabrik/lfops/tree/main/roles/sshd): `fail2ban__skip_sshd`
* [repo_epel](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_epel): `fail2ban__skip_repo_epel`
* [firewall](https://github.com/Linuxfabrik/lfops/tree/main/roles/firewall): `fail2ban__skip_firewall`
* [fail2ban](https://github.com/Linuxfabrik/lfops/tree/main/roles/fail2ban)


## fangfrisch.yml

Calls the following roles (in order):

* [python_venv](https://github.com/Linuxfabrik/lfops/tree/main/roles/python_venv): `clamav__skip_python_venv`
* [fangfrisch](https://github.com/Linuxfabrik/lfops/tree/main/roles/fangfrisch)


## ffmpeg.yml

Calls the following roles (in order):

* [repo_baseos](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_baseos): `ffmpeg__skip_repo_baseos`
* [repo_epel](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_epel): `ffmpeg__skip_repo_epel`
* [repo_rpmfusion](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_rpmfusion): `ffmpeg__skip_repo_rpmfusion`
* [apps](https://github.com/Linuxfabrik/lfops/tree/main/roles/apps)


## files.yml

Calls the following roles (in order):

* [files](https://github.com/Linuxfabrik/lfops/tree/main/roles/files)


## firewall.yml

Calls the following roles (in order):

* [firewall](https://github.com/Linuxfabrik/lfops/tree/main/roles/firewall)


## freeipa_client.yml

Calls the following roles (in order):

* [freeipa_client](https://github.com/Linuxfabrik/lfops/tree/main/roles/freeipa_client)


## freeipa_server.yml

Calls the following roles (in order):

* [freeipa_server](https://github.com/Linuxfabrik/lfops/tree/main/roles/freeipa_server)


## github_project_createrepo.yml

Calls the following roles (in order):

* [apps](https://github.com/Linuxfabrik/lfops/tree/main/roles/apps): `github_project_createrepo__skip_apps`
* [python](https://github.com/Linuxfabrik/lfops/tree/main/roles/python): `github_project_createrepo__skip_python`
* [github_project_createrepo](https://github.com/Linuxfabrik/lfops/tree/main/roles/github_project_createrepo)


## gitlab_ce.yml

Calls the following roles (in order):

* [policycoreutils](https://github.com/Linuxfabrik/lfops/tree/main/roles/policycoreutils)
* [kernel_settings](https://github.com/Linuxfabrik/lfops/tree/main/roles/kernel_settings): `gitlab_ce__skip_kernel_settings`
* [repo_gitlab_ce](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_gitlab_ce): `gitlab_ce__skip_repo_gitlab_ce`
* [apps](https://github.com/Linuxfabrik/lfops/tree/main/roles/apps)
* [gitlab_ce](https://github.com/Linuxfabrik/lfops/tree/main/roles/gitlab_ce)


## glances.yml

Calls the following roles (in order):

* [repo_baseos](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_baseos): `glances__skip_repo_baseos`
* [repo_epel](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_epel)
* [glances](https://github.com/Linuxfabrik/lfops/tree/main/roles/glances)


## glpi_agent.yml

Calls the following roles (in order):

* [repo_baseos](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_baseos): `glpi_agent__skip_repo_baseos`
* [repo_epel](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_epel): `glpi_agent__skip_repo_epel`
* [glpi_agent](https://github.com/Linuxfabrik/lfops/tree/main/roles/glpi_agent)


## grafana.yml

Calls the following roles (in order):

* [repo_grafana](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_grafana): `grafana_server__skip_repo_grafana`
* [grafana](https://github.com/Linuxfabrik/lfops/tree/main/roles/grafana)


## grafana_grizzly.yml

Calls the following roles (in order):

* [repo_grafana](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_grafana): `grafana_server__skip_repo_grafana`
* [grafana](https://github.com/Linuxfabrik/lfops/tree/main/roles/grafana): `grafana_server__skip_grafana`
* [grafana_grizzly](https://github.com/Linuxfabrik/lfops/tree/main/roles/grafana_grizzly)


## haveged.yml

Calls the following roles (in order):

* [haveged](https://github.com/Linuxfabrik/lfops/tree/main/roles/haveged)


## hetzner_vm.yml

Calls the following roles (in order):

* [hetzner_vm](https://github.com/Linuxfabrik/lfops/tree/main/roles/hetzner_vm)


## hostname.yml

Calls the following roles (in order):

* [hostname](https://github.com/Linuxfabrik/lfops/tree/main/roles/hostname)


## icinga2_agent.yml

Calls the following roles (in order):

* [repo_baseos](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_baseos): `icinga2_agent__skip_repo_baseos`
* [repo_icinga](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_icinga): `icinga2_agent__skip_repo_icinga`
* [icinga2_agent](https://github.com/Linuxfabrik/lfops/tree/main/roles/icinga2_agent)
* [repo_epel](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_epel): `icinga2_agent__skip_repo_epel` (default: `true`)
* [repo_monitoring_plugins](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_monitoring_plugins): `icinga2_agent__skip_repo_monitoring_plugins`
* [monitoring_plugins](https://github.com/Linuxfabrik/lfops/tree/main/roles/monitoring_plugins): `icinga2_agent__skip_monitoring_plugins`


## icingaweb2.yml

Calls the following roles (in order):

* [repo_baseos](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_baseos): `icingaweb2__skip_repo_baseos`
* [kernel_settings](https://github.com/Linuxfabrik/lfops/tree/main/roles/kernel_settings): `icingaweb2__skip_kernel_settings`
* [repo_epel](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_epel)
* [repo_mydumper](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_mydumper): `icingaweb2__skip_repo_mydumper`
* [repo_mariadb](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_mariadb): `icingaweb2__skip_repo_mariadb`
* [python](https://github.com/Linuxfabrik/lfops/tree/main/roles/python): `icingaweb2__skip_python`
* [mariadb_server](https://github.com/Linuxfabrik/lfops/tree/main/roles/mariadb_server): `icingaweb2__skip_mariadb_server`
* [yum_utils](https://github.com/Linuxfabrik/lfops/tree/main/roles/yum_utils): `icingaweb2__skip_yum_utils`
* [repo_remi](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_remi): `icingaweb2__skip_repo_remi`
* [php](https://github.com/Linuxfabrik/lfops/tree/main/roles/php): `icingaweb2__skip_php`
* [repo_icinga](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_icinga): `icingaweb2__skip_repo_icinga`
* [icingaweb2](https://github.com/Linuxfabrik/lfops/tree/main/roles/icingaweb2)


## icingaweb2_module_businessprocess.yml

Calls the following roles (in order):

* [icingaweb2_module_businessprocess](https://github.com/Linuxfabrik/lfops/tree/main/roles/icingaweb2_module_businessprocess)


## icingaweb2_module_company.yml

Calls the following roles (in order):

* [icingaweb2_module_company](https://github.com/Linuxfabrik/lfops/tree/main/roles/icingaweb2_module_company)


## icingaweb2_module_director.yml

Calls the following roles (in order):

* [icingaweb2_module_director](https://github.com/Linuxfabrik/lfops/tree/main/roles/icingaweb2_module_director)


## icingaweb2_module_doc.yml

Calls the following roles (in order):

* [icingaweb2_module_doc](https://github.com/Linuxfabrik/lfops/tree/main/roles/icingaweb2_module_doc)


## icingaweb2_module_incubator.yml

Calls the following roles (in order):

* [icingaweb2_module_incubator](https://github.com/Linuxfabrik/lfops/tree/main/roles/icingaweb2_module_incubator)


## icingaweb2_module_pdfexport.yml

Calls the following roles (in order):

* [icingaweb2_module_pdfexport](https://github.com/Linuxfabrik/lfops/tree/main/roles/icingaweb2_module_pdfexport)


## influxdb.yml

Calls the following roles (in order):

* [repo_influxdb](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_influxdb)
* [python_venv](https://github.com/Linuxfabrik/lfops/tree/main/roles/python_venv): `influxdb__skip_python_venv`
* [influxdb](https://github.com/Linuxfabrik/lfops/tree/main/roles/influxdb)


## infomaniak_vm.yml

Calls the following roles (in order):

* [infomaniak_vm](https://github.com/Linuxfabrik/lfops/tree/main/roles/infomaniak_vm)


## kdump.yml

Calls the following roles (in order):

* [kdump](https://github.com/Linuxfabrik/lfops/tree/main/roles/kdump)


## keepalived.yml

Calls the following roles (in order):

* [keepalived](https://github.com/Linuxfabrik/lfops/tree/main/roles/keepalived)


## kernel_settings.yml

Calls the following roles (in order):

* [kernel_settings](https://github.com/Linuxfabrik/lfops/tree/main/roles/kernel_settings)


## kibana.yml

Calls the following roles (in order):

* [repo_elasticsearch](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_elasticsearch): `kibana__skip_repo_elasticsearch`
* [kibana](https://github.com/Linuxfabrik/lfops/tree/main/roles/kibana)


## kvm_host.yml

Calls the following roles (in order):

* [python](https://github.com/Linuxfabrik/lfops/tree/main/roles/python): `kvm_host__skip_python`
* [kvm_host](https://github.com/Linuxfabrik/lfops/tree/main/roles/kvm_host)


## libmaxminddb.yml

Calls the following roles (in order):

* [libmaxminddb](https://github.com/Linuxfabrik/lfops/tree/main/roles/libmaxminddb)


## libreoffice.yml

Calls the following roles (in order):

* [selinux](https://github.com/Linuxfabrik/lfops/tree/main/roles/selinux)
* [libreoffice](https://github.com/Linuxfabrik/lfops/tree/main/roles/libreoffice)


## login.yml

Calls the following roles (in order):

* [login](https://github.com/Linuxfabrik/lfops/tree/main/roles/login)


## logrotate.yml

Calls the following roles (in order):

* [logrotate](https://github.com/Linuxfabrik/lfops/tree/main/roles/logrotate)


## logstash.yml

Calls the following roles (in order):

* [repo_elasticsearch](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_elasticsearch): `logstash__skip_repo_elasticsearch`
* [logstash](https://github.com/Linuxfabrik/lfops/tree/main/roles/logstash)


## lvm.yml

Calls the following roles (in order):

* [lvm](https://github.com/Linuxfabrik/lfops/tree/main/roles/lvm)


## mailto_root.yml

Calls the following roles (in order):

* [repo_baseos](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_baseos): `mailto_root__skip_repo_baseos`
* [repo_epel](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_epel)
* [postfix](https://github.com/Linuxfabrik/lfops/tree/main/roles/postfix): `mailto_root__skip_postfix`
* [mailx](https://github.com/Linuxfabrik/lfops/tree/main/roles/mailx): `mailto_root__skip_mailx`
* [mailto_root](https://github.com/Linuxfabrik/lfops/tree/main/roles/mailto_root)


## mailx.yml

Calls the following roles (in order):

* [mailx](https://github.com/Linuxfabrik/lfops/tree/main/roles/mailx)


## mariadb_server.yml

Calls the following roles (in order):

* [repo_baseos](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_baseos): `mariadb_server__skip_repo_baseos`
* [kernel_settings](https://github.com/Linuxfabrik/lfops/tree/main/roles/kernel_settings): `mariadb_server__skip_kernel_settings`
* [repo_epel](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_epel): `mariadb_server__skip_repo_epel`
* [repo_mydumper](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_mydumper): `mariadb_server__skip_repo_mydumper`
* [repo_mariadb](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_mariadb): `mariadb_server__skip_repo_mariadb`
* [python](https://github.com/Linuxfabrik/lfops/tree/main/roles/python): `mariadb_server__skip_python`
* [policycoreutils](https://github.com/Linuxfabrik/lfops/tree/main/roles/policycoreutils): `mariadb_server__skip_policycoreutils`
* [mariadb_server](https://github.com/Linuxfabrik/lfops/tree/main/roles/mariadb_server)


## maxmind_geoip.yml

Calls the following roles (in order):

* [maxmind_geoip](https://github.com/Linuxfabrik/lfops/tree/main/roles/maxmind_geoip)
* [systemd_unit](https://github.com/Linuxfabrik/lfops/tree/main/roles/systemd_unit): `maxmind_geoip__skip_systemd_unit`


## minio_client.yml

Calls the following roles (in order):

* [minio_client](https://github.com/Linuxfabrik/lfops/tree/main/roles/minio_client)


## mirror.yml

Calls the following roles (in order):

* [apps](https://github.com/Linuxfabrik/lfops/tree/main/roles/apps): `mirror__skip_apps`
* [yum_utils](https://github.com/Linuxfabrik/lfops/tree/main/roles/yum_utils): `mirror__skip_yum_utils`
* [python](https://github.com/Linuxfabrik/lfops/tree/main/roles/python): `mirror__skip_python`
* [mirror](https://github.com/Linuxfabrik/lfops/tree/main/roles/mirror)


## mod_maxminddb.yml

Calls the following roles (in order):

* [mod_maxminddb](https://github.com/Linuxfabrik/lfops/tree/main/roles/mod_maxminddb)


## mongodb.yml

Calls the following roles (in order):

* [kernel_settings](https://github.com/Linuxfabrik/lfops/tree/main/roles/kernel_settings): `mongodb__skip_kernel_settings`
* [python_venv](https://github.com/Linuxfabrik/lfops/tree/main/roles/python_venv): `mongodb__skip_python_venv`
* [repo_mongodb](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_mongodb): `mongodb__skip_repo_mongodb`
* [mongodb](https://github.com/Linuxfabrik/lfops/tree/main/roles/mongodb)


## monitoring_plugins.yml

Calls the following roles (in order):

* [repo_monitoring_plugins](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_monitoring_plugins): `monitoring_plugins__skip_repo_monitoring_plugins`
* [monitoring_plugins](https://github.com/Linuxfabrik/lfops/tree/main/roles/monitoring_plugins)


## monitoring_plugins_grafana_dashboards.yml

Calls the following roles (in order):

* [repo_grafana](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_grafana): `monitoring_plugins_grafana_dashboards__skip_repo_grafana`
* [grafana](https://github.com/Linuxfabrik/lfops/tree/main/roles/grafana): `monitoring_plugins_grafana_dashboards__skip_grafana`, `monitoring_plugins_grafana_dashboards__skip_grafana_grizzly`
* [grafana_grizzly](https://github.com/Linuxfabrik/lfops/tree/main/roles/grafana_grizzly): `monitoring_plugins_grafana_dashboards__skip_grafana_grizzly`
* [monitoring_plugins_grafana_dashboards](https://github.com/Linuxfabrik/lfops/tree/main/roles/monitoring_plugins_grafana_dashboards)


## motd.yml

Calls the following roles (in order):

* [motd](https://github.com/Linuxfabrik/lfops/tree/main/roles/motd)


## mount.yml

Calls the following roles (in order):

* [mount](https://github.com/Linuxfabrik/lfops/tree/main/roles/mount)


## network.yml

Calls the following roles (in order):

* [network](https://github.com/Linuxfabrik/lfops/tree/main/roles/network)


## nfs_client.yml

Calls the following roles (in order):

* [nfs_client](https://github.com/Linuxfabrik/lfops/tree/main/roles/nfs_client)


## nfs_server.yml

Calls the following roles (in order):

* [nfs_server](https://github.com/Linuxfabrik/lfops/tree/main/roles/nfs_server)


## nodejs.yml

Calls the following roles (in order):

* [nodejs](https://github.com/Linuxfabrik/lfops/tree/main/roles/nodejs)


## objectstore_backup.yml

Calls the following roles (in order):

* [minio_client](https://github.com/Linuxfabrik/lfops/tree/main/roles/minio_client): `objectstore_backup__skip_minio_client`
* [objectstore_backup](https://github.com/Linuxfabrik/lfops/tree/main/roles/objectstore_backup)


## open_vm_tools.yml

Calls the following roles (in order):

* [open_vm_tools](https://github.com/Linuxfabrik/lfops/tree/main/roles/open_vm_tools)


## opensearch.yml

Calls the following roles (in order):

* [repo_opensearch](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_opensearch): `opensearch__skip_repo_opensearch`
* [opensearch](https://github.com/Linuxfabrik/lfops/tree/main/roles/opensearch)


## openvpn_server.yml

Calls the following roles (in order):

* [repo_baseos](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_baseos): `openvpn_server__skip_repo_baseos`
* [repo_epel](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_epel): `openvpn_server__skip_repo_epel`
* [policycoreutils](https://github.com/Linuxfabrik/lfops/tree/main/roles/policycoreutils): `openvpn_server__skip_policycoreutils`
* [openvpn_server](https://github.com/Linuxfabrik/lfops/tree/main/roles/openvpn_server)


## php.yml

Calls the following roles (in order):

* [yum_utils](https://github.com/Linuxfabrik/lfops/tree/main/roles/yum_utils): `php__skip_yum_utils`
* [repo_remi](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_remi): `php__skip_repo_remi`
* [php](https://github.com/Linuxfabrik/lfops/tree/main/roles/php)


## podman_containers.yml

Calls the following roles (in order):

* [podman_containers](https://github.com/Linuxfabrik/lfops/tree/main/roles/podman_containers)


## policycoreutils.yml

Calls the following roles (in order):

* [policycoreutils](https://github.com/Linuxfabrik/lfops/tree/main/roles/policycoreutils)


## postfix.yml

Calls the following roles (in order):

* [mailx](https://github.com/Linuxfabrik/lfops/tree/main/roles/mailx): `postfix__skip_mailx`
* [postfix](https://github.com/Linuxfabrik/lfops/tree/main/roles/postfix)


## postgresql_server.yml

Calls the following roles (in order):

* [python](https://github.com/Linuxfabrik/lfops/tree/main/roles/python): `postgresql_server__skip_python`
* [repo_postgresql](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_postgresql): `postgresql_server__skip_repo_postgresql`
* [postgresql_server](https://github.com/Linuxfabrik/lfops/tree/main/roles/postgresql_server)


## proxysql.yml

Calls the following roles (in order):

* [repo_proxysql](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_proxysql): `proxysql__skip_repo_proxysql`
* [proxysql](https://github.com/Linuxfabrik/lfops/tree/main/roles/proxysql)


## python.yml

Calls the following roles (in order):

* [python](https://github.com/Linuxfabrik/lfops/tree/main/roles/python)


## python_venv.yml

Calls the following roles (in order):

* [python](https://github.com/Linuxfabrik/lfops/tree/main/roles/python): `python_venv__skip_python`
* [python_venv](https://github.com/Linuxfabrik/lfops/tree/main/roles/python_venv)


## qemu_guest_agent.yml

Calls the following roles (in order):

* [qemu_guest_agent](https://github.com/Linuxfabrik/lfops/tree/main/roles/qemu_guest_agent)


## redis.yml

Calls the following roles (in order):

* [kernel_settings](https://github.com/Linuxfabrik/lfops/tree/main/roles/kernel_settings): `redis__skip_kernel_settings`
* [repo_remi](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_remi): `redis__skip_repo_remi`
* [repo_redis](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_redis)
* [redis](https://github.com/Linuxfabrik/lfops/tree/main/roles/redis)


## repo_baseos.yml

Calls the following roles (in order):

* [repo_baseos](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_baseos)


## repo_collabora.yml

Calls the following roles (in order):

* [repo_collabora](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_collabora)


## repo_collabora_code.yml

Calls the following roles (in order):

* [repo_collabora_code](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_collabora_code)


## repo_debian_base.yml

Calls the following roles (in order):

* [repo_debian_base](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_debian_base)


## repo_docker.yml

Calls the following roles (in order):

* [repo_docker](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_docker)


## repo_elasticsearch.yml

Calls the following roles (in order):

* [repo_elasticsearch](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_elasticsearch)


## repo_epel.yml

Calls the following roles (in order):

* [repo_epel](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_epel)


## repo_gitlab_ce.yml

Calls the following roles (in order):

* [repo_gitlab_ce](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_gitlab_ce)


## repo_gitlab_runner.yml

Calls the following roles (in order):

* [repo_gitlab_runner](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_gitlab_runner)


## repo_grafana.yml

Calls the following roles (in order):

* [repo_grafana](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_grafana)


## repo_graylog.yml

Calls the following roles (in order):

* [repo_graylog](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_graylog)


## repo_icinga.yml

Calls the following roles (in order):

* [repo_icinga](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_icinga)


## repo_influxdb.yml

Calls the following roles (in order):

* [repo_influxdb](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_influxdb)


## repo_mariadb.yml

Calls the following roles (in order):

* [repo_mariadb](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_mariadb)


## repo_mongodb.yml

Calls the following roles (in order):

* [repo_mongodb](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_mongodb)


## repo_monitoring_plugins.yml

Calls the following roles (in order):

* [repo_monitoring_plugins](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_monitoring_plugins)


## repo_mydumper.yml

Calls the following roles (in order):

* [repo_mydumper](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_mydumper)


## repo_opensearch.yml

Calls the following roles (in order):

* [repo_opensearch](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_opensearch)


## repo_postgresql.yml

Calls the following roles (in order):

* [repo_postgresql](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_postgresql)


## repo_proxysql.yml

Calls the following roles (in order):

* [repo_proxysql](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_proxysql)


## repo_redis.yml

Calls the following roles (in order):

* [repo_redis](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_redis)


## repo_remi.yml

Calls the following roles (in order):

* [yum_utils](https://github.com/Linuxfabrik/lfops/tree/main/roles/yum_utils)
* [repo_baseos](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_baseos): `repo_remi__skip_repo_baseos`
* [repo_epel](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_epel)
* [repo_remi](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_remi)


## repo_rpmfusion.yml

Calls the following roles (in order):

* [repo_baseos](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_baseos): `repo_rpmfusion__skip_repo_baseos`
* [repo_epel](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_epel): `repo_rpmfusion__skip_repo_epel`
* [repo_rpmfusion](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_rpmfusion)


## repo_sury.yml

Calls the following roles (in order):

* [repo_sury](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_sury)


## rsyslog.yml

Calls the following roles (in order):

* [rsyslog](https://github.com/Linuxfabrik/lfops/tree/main/roles/rsyslog)


## selinux.yml

Calls the following roles (in order):

* [policycoreutils](https://github.com/Linuxfabrik/lfops/tree/main/roles/policycoreutils): `selinux__skip_policycoreutils`
* [selinux](https://github.com/Linuxfabrik/lfops/tree/main/roles/selinux)


## setup_basic.yml

Calls the following roles (in order):

* [network](https://github.com/Linuxfabrik/lfops/tree/main/roles/network): `setup_basic__skip_network`
* [repo_baseos](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_baseos): `setup_basic__skip_repo_baseos`
* [repo_epel](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_epel): `setup_basic__skip_repo_epel`
* [crypto_policy](https://github.com/Linuxfabrik/lfops/tree/main/roles/crypto_policy): `setup_basic__skip_crypto_policy`
* [policycoreutils](https://github.com/Linuxfabrik/lfops/tree/main/roles/policycoreutils)
* [selinux](https://github.com/Linuxfabrik/lfops/tree/main/roles/selinux): `setup_basic__skip_selinux`
* [systemd_journald](https://github.com/Linuxfabrik/lfops/tree/main/roles/systemd_journald): `setup_basic__skip_systemd_journald`
* [hostname](https://github.com/Linuxfabrik/lfops/tree/main/roles/hostname): `setup_basic__skip_hostname`
* [timezone](https://github.com/Linuxfabrik/lfops/tree/main/roles/timezone): `setup_basic__skip_timezone`
* [logrotate](https://github.com/Linuxfabrik/lfops/tree/main/roles/logrotate): `setup_basic__skip_logrotate`
* [rsyslog](https://github.com/Linuxfabrik/lfops/tree/main/roles/rsyslog): `setup_basic__skip_rsyslog`
* [cloud_init](https://github.com/Linuxfabrik/lfops/tree/main/roles/cloud_init): `setup_basic__skip_cloud_init`
* [cockpit](https://github.com/Linuxfabrik/lfops/tree/main/roles/cockpit): `setup_basic__skip_cockpit`
* [dnf_makecache](https://github.com/Linuxfabrik/lfops/tree/main/roles/dnf_makecache): `setup_basic__skip_dnf_makecache`
* [kdump](https://github.com/Linuxfabrik/lfops/tree/main/roles/kdump): `setup_basic__skip_kdump`
* [chrony](https://github.com/Linuxfabrik/lfops/tree/main/roles/chrony): `setup_basic__skip_chrony`
* [motd](https://github.com/Linuxfabrik/lfops/tree/main/roles/motd): `setup_basic__skip_motd`
* [python](https://github.com/Linuxfabrik/lfops/tree/main/roles/python): `setup_basic__skip_python`, `setup_basic__skip_python_venv`
* [glances](https://github.com/Linuxfabrik/lfops/tree/main/roles/glances): `setup_basic__skip_glances`
* [tools](https://github.com/Linuxfabrik/lfops/tree/main/roles/tools): `setup_basic__skip_tools`
* [at](https://github.com/Linuxfabrik/lfops/tree/main/roles/at): `setup_basic__skip_at`
* [yum_utils](https://github.com/Linuxfabrik/lfops/tree/main/roles/yum_utils): `setup_basic__skip_yum_utils`
* [lvm](https://github.com/Linuxfabrik/lfops/tree/main/roles/lvm): `setup_basic__skip_lvm`
* [sshd](https://github.com/Linuxfabrik/lfops/tree/main/roles/sshd): `setup_basic__skip_sshd`
* [login](https://github.com/Linuxfabrik/lfops/tree/main/roles/login): `setup_basic__skip_login`
* [firewall](https://github.com/Linuxfabrik/lfops/tree/main/roles/firewall): `setup_basic__skip_firewall`
* [mailx](https://github.com/Linuxfabrik/lfops/tree/main/roles/mailx): `setup_basic__skip_mailx`
* [postfix](https://github.com/Linuxfabrik/lfops/tree/main/roles/postfix): `setup_basic__skip_postfix`
* [mailto_root](https://github.com/Linuxfabrik/lfops/tree/main/roles/mailto_root): `setup_basic__skip_mailto_root`
* [system_update](https://github.com/Linuxfabrik/lfops/tree/main/roles/system_update): `setup_basic__skip_system_update`
* [python_venv](https://github.com/Linuxfabrik/lfops/tree/main/roles/python_venv): `setup_basic__skip_python_venv`
* [duplicity](https://github.com/Linuxfabrik/lfops/tree/main/roles/duplicity): `setup_basic__skip_duplicity`
* [repo_monitoring_plugins](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_monitoring_plugins): `setup_basic__skip_repo_monitoring_plugins`
* [monitoring_plugins](https://github.com/Linuxfabrik/lfops/tree/main/roles/monitoring_plugins): `setup_basic__skip_monitoring_plugins`
* [repo_icinga](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_icinga): `setup_basic__skip_repo_icinga`
* [icinga2_agent](https://github.com/Linuxfabrik/lfops/tree/main/roles/icinga2_agent): `setup_basic__skip_icinga2_agent`


## setup_grav.yml

Calls the following roles (in order):

* [yum_utils](https://github.com/Linuxfabrik/lfops/tree/main/roles/yum_utils): `grav__skip_yum_utils`
* [policycoreutils](https://github.com/Linuxfabrik/lfops/tree/main/roles/policycoreutils): `grav__skip_policycoreutils`
* [apps](https://github.com/Linuxfabrik/lfops/tree/main/roles/apps): `grav__skip_apps`
* [repo_remi](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_remi): `grav__skip_repo_remi`
* [php](https://github.com/Linuxfabrik/lfops/tree/main/roles/php): `grav__skip_php`
* [selinux](https://github.com/Linuxfabrik/lfops/tree/main/roles/selinux): `setup_grav__skip_selinux`
* [python](https://github.com/Linuxfabrik/lfops/tree/main/roles/python): `grav__skip_python`
* [apache_httpd](https://github.com/Linuxfabrik/lfops/tree/main/roles/apache_httpd): `grav__skip_apache_httpd`
* [grav](https://github.com/Linuxfabrik/lfops/tree/main/roles/grav)


## setup_graylog_datanode.yml

Calls the following roles (in order):

* [policycoreutils](https://github.com/Linuxfabrik/lfops/tree/main/roles/policycoreutils): `setup_graylog_datanode__skip_policycoreutils`
* [repo_baseos](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_baseos): `setup_graylog_datanode__skip_repo_baseos`
* [repo_epel](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_epel)
* [python_venv](https://github.com/Linuxfabrik/lfops/tree/main/roles/python_venv): `setup_graylog_datanode__skip_python_venv`
* [repo_mongodb](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_mongodb): `setup_graylog_datanode__skip_repo_mongodb`
* [kernel_settings](https://github.com/Linuxfabrik/lfops/tree/main/roles/kernel_settings): `setup_graylog_datanode__skip_kernel_settings`
* [mongodb](https://github.com/Linuxfabrik/lfops/tree/main/roles/mongodb): `setup_graylog_datanode__skip_mongodb`
* [repo_graylog](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_graylog): `setup_graylog_datanode__skip_repo_graylog`
* [selinux](https://github.com/Linuxfabrik/lfops/tree/main/roles/selinux): `setup_graylog_datanode__skip_selinux`
* [graylog_datanode](https://github.com/Linuxfabrik/lfops/tree/main/roles/graylog_datanode)


## setup_graylog_server.yml

Calls the following roles (in order):

* [policycoreutils](https://github.com/Linuxfabrik/lfops/tree/main/roles/policycoreutils): `setup_graylog_server__skip_policycoreutils`
* [selinux](https://github.com/Linuxfabrik/lfops/tree/main/roles/selinux): `setup_graylog_server__skip_selinux`
* [repo_baseos](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_baseos): `setup_graylog_server__skip_repo_baseos`
* [repo_epel](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_epel)
* [python_venv](https://github.com/Linuxfabrik/lfops/tree/main/roles/python_venv): `setup_graylog_server__skip_python_venv`
* [repo_mongodb](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_mongodb): `setup_graylog_server__skip_repo_mongodb`
* [kernel_settings](https://github.com/Linuxfabrik/lfops/tree/main/roles/kernel_settings): `setup_graylog_server__skip_kernel_settings`
* [mongodb](https://github.com/Linuxfabrik/lfops/tree/main/roles/mongodb): `setup_graylog_server__skip_mongodb`
* [repo_graylog](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_graylog): `setup_graylog_server__skip_repo_graylog`
* [graylog_datanode](https://github.com/Linuxfabrik/lfops/tree/main/roles/graylog_datanode): `setup_graylog_server__skip_graylog_datanode`
* [graylog_server](https://github.com/Linuxfabrik/lfops/tree/main/roles/graylog_server)


## setup_icinga2_master.yml

Calls the following roles (in order):

* [repo_baseos](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_baseos): `setup_icinga2_master__skip_repo_baseos`
* [repo_epel](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_epel): `setup_icinga2_master__repo_epel__skip_role`
* [repo_mariadb](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_mariadb): `setup_icinga2_master__repo_mariadb__skip_role`
* [python](https://github.com/Linuxfabrik/lfops/tree/main/roles/python): `setup_icinga2_master__python__skip_role`
* [repo_mydumper](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_mydumper): `setup_icinga2_master__repo_mydumper__skip_role`
* [policycoreutils](https://github.com/Linuxfabrik/lfops/tree/main/roles/policycoreutils): `setup_icinga2_master__policycoreutils__skip_role`
* [mariadb_server](https://github.com/Linuxfabrik/lfops/tree/main/roles/mariadb_server): `setup_icinga2_master__mariadb_server__skip_role`
* [repo_influxdb](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_influxdb): `setup_icinga2_master__repo_influxdb__skip_role`
* [python_venv](https://github.com/Linuxfabrik/lfops/tree/main/roles/python_venv): `setup_icinga2_master__python_venv__skip_role`
* [repo_icinga](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_icinga): `setup_icinga2_master__repo_icinga__skip_role`
* [icinga2_master](https://github.com/Linuxfabrik/lfops/tree/main/roles/icinga2_master): `setup_icinga2_master__icinga2_master__skip_role`
* [yum_utils](https://github.com/Linuxfabrik/lfops/tree/main/roles/yum_utils): `setup_icinga2_master__yum_utils__skip_role`
* [repo_remi](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_remi): `setup_icinga2_master__repo_remi__skip_role`
* [repo_sury](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_sury): `setup_icinga2_master__repo_sury__skip_role`
* [php](https://github.com/Linuxfabrik/lfops/tree/main/roles/php): `setup_icinga2_master__php__skip_role`
* [apache_httpd](https://github.com/Linuxfabrik/lfops/tree/main/roles/apache_httpd): `setup_icinga2_master__apache_httpd__skip_role`
* [icingaweb2](https://github.com/Linuxfabrik/lfops/tree/main/roles/icingaweb2): `setup_icinga2_master__icingaweb2__skip_role`
* [repo_monitoring_plugins](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_monitoring_plugins): `setup_icinga2_master__repo_monitoring_plugins__skip_role`
* [monitoring_plugins](https://github.com/Linuxfabrik/lfops/tree/main/roles/monitoring_plugins): `setup_icinga2_master__monitoring_plugins__skip_role`
* [selinux](https://github.com/Linuxfabrik/lfops/tree/main/roles/selinux): `setup_icinga2_master__selinux__skip_role`
* [kernel_settings](https://github.com/Linuxfabrik/lfops/tree/main/roles/kernel_settings): `setup_icinga2_master__kernel_settings__skip_role`
* [repo_redis](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_redis): `setup_icinga2_master__repo_redis__skip_role`
* [redis](https://github.com/Linuxfabrik/lfops/tree/main/roles/redis): `setup_icinga2_master__redis__skip_role`
* [icingadb](https://github.com/Linuxfabrik/lfops/tree/main/roles/icingadb): `setup_icinga2_master__icingadb__skip_role`
* [icinga_kubernetes](https://github.com/Linuxfabrik/lfops/tree/main/roles/icinga_kubernetes): `setup_icinga2_master__icinga_kubernetes__skip_role` (default: `true`)
* [icinga_kubernetes_web](https://github.com/Linuxfabrik/lfops/tree/main/roles/icinga_kubernetes_web): `setup_icinga2_master__icinga_kubernetes_web__skip_role` (default: `true`)
* [icingadb_web](https://github.com/Linuxfabrik/lfops/tree/main/roles/icingadb_web): `setup_icinga2_master__icingadb_web__skip_role`
* [icingaweb2_module_doc](https://github.com/Linuxfabrik/lfops/tree/main/roles/icingaweb2_module_doc): `setup_icinga2_master__icingaweb2_module_doc__skip_role`
* [icingaweb2_module_fileshipper](https://github.com/Linuxfabrik/lfops/tree/main/roles/icingaweb2_module_fileshipper): `setup_icinga2_master__icingaweb2_module_fileshipper__skip_role` (default: `true`)
* [icingaweb2_module_generictts](https://github.com/Linuxfabrik/lfops/tree/main/roles/icingaweb2_module_generictts): `setup_icinga2_master__icingaweb2_module_generictts__skip_role` (default: `true`)
* [icingaweb2_module_x509](https://github.com/Linuxfabrik/lfops/tree/main/roles/icingaweb2_module_x509): `setup_icinga2_master__icingaweb2_module_x509__skip_role` (default: `true`)
* [icingaweb2_module_reporting](https://github.com/Linuxfabrik/lfops/tree/main/roles/icingaweb2_module_reporting): `setup_icinga2_master__icingaweb2_module_reporting__skip_role` (default: `true`)
* [icingaweb2_module_businessprocess](https://github.com/Linuxfabrik/lfops/tree/main/roles/icingaweb2_module_businessprocess): `setup_icinga2_master__icingaweb2_module_businessprocess__skip_role` (default: `true`)
* [icingaweb2_module_company](https://github.com/Linuxfabrik/lfops/tree/main/roles/icingaweb2_module_company): `setup_icinga2_master__icingaweb2_module_company__skip_role` (default: `true`)
* [icingaweb2_module_cube](https://github.com/Linuxfabrik/lfops/tree/main/roles/icingaweb2_module_cube): `setup_icinga2_master__icingaweb2_module_cube__skip_role` (default: `true`)
* [icingaweb2_theme_linuxfabrik](https://github.com/Linuxfabrik/lfops/tree/main/roles/icingaweb2_theme_linuxfabrik): `setup_icinga2_master__icingaweb2_theme_linuxfabrik__skip_role`
* [icingaweb2_module_incubator](https://github.com/Linuxfabrik/lfops/tree/main/roles/icingaweb2_module_incubator): `setup_icinga2_master__icingaweb2_module_incubator__skip_role`
* [icingaweb2_module_jira](https://github.com/Linuxfabrik/lfops/tree/main/roles/icingaweb2_module_jira): `setup_icinga2_master__icingaweb2_module_jira__skip_role` (default: `true`)
* [icingaweb2_module_pdfexport](https://github.com/Linuxfabrik/lfops/tree/main/roles/icingaweb2_module_pdfexport): `setup_icinga2_master__icingaweb2_module_pdfexport__skip_role` (default: `true`)
* [icingaweb2_module_vspheredb](https://github.com/Linuxfabrik/lfops/tree/main/roles/icingaweb2_module_vspheredb): `setup_icinga2_master__icingaweb2_module_vspheredb__skip_role` (default: `true`)
* [icingaweb2_module_director](https://github.com/Linuxfabrik/lfops/tree/main/roles/icingaweb2_module_director): `setup_icinga2_master__icingaweb2_module_director__skip_role`
* [repo_grafana](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_grafana): `setup_icinga2_master__repo_grafana__skip_role`
* [grafana](https://github.com/Linuxfabrik/lfops/tree/main/roles/grafana): `setup_icinga2_master__grafana__skip_role`
* [grafana_grizzly](https://github.com/Linuxfabrik/lfops/tree/main/roles/grafana_grizzly): `setup_icinga2_master__grafana_grizzly__skip_role`
* [influxdb](https://github.com/Linuxfabrik/lfops/tree/main/roles/influxdb): `setup_icinga2_master__influxdb__skip_role`
* [icingaweb2_module_grafana](https://github.com/Linuxfabrik/lfops/tree/main/roles/icingaweb2_module_grafana): `setup_icinga2_master__icingaweb2_module_grafana__skip_role`
* [monitoring_plugins_grafana_dashboards](https://github.com/Linuxfabrik/lfops/tree/main/roles/monitoring_plugins_grafana_dashboards): `setup_icinga2_master__monitoring_plugins_grafana_dashboards__skip_role`


## setup_keycloak.yml

Calls the following roles (in order):

* [repo_baseos](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_baseos): `setup_keycloak__skip_repo_baseos`
* [repo_epel](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_epel)
* [repo_mydumper](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_mydumper): `keycloak__skip_repo_mydumper`
* [repo_mariadb](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_mariadb): `mariadb_server__skip_repo_mariadb`
* [python](https://github.com/Linuxfabrik/lfops/tree/main/roles/python): `mariadb_server__skip_python`
* [kernel_settings](https://github.com/Linuxfabrik/lfops/tree/main/roles/kernel_settings): `keycloak__skip_kernel_settings`
* [policycoreutils](https://github.com/Linuxfabrik/lfops/tree/main/roles/policycoreutils): `keycloak__skip_policycoreutils`
* [mariadb_server](https://github.com/Linuxfabrik/lfops/tree/main/roles/mariadb_server)
* [apps](https://github.com/Linuxfabrik/lfops/tree/main/roles/apps)
* [keycloak](https://github.com/Linuxfabrik/lfops/tree/main/roles/keycloak)


## setup_librenms.yml

Calls the following roles (in order):

* [yum_utils](https://github.com/Linuxfabrik/lfops/tree/main/roles/yum_utils): `librenms__skip_yum_utils`
* [repo_baseos](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_baseos): `setup_librenms__skip_repo_baseos`
* [repo_epel](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_epel): `librenms__skip_repo_epel`
* [repo_mydumper](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_mydumper): `librenms__skip_repo_mydumper`
* [repo_mariadb](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_mariadb): `librenms__skip_repo_mariadb`
* [policycoreutils](https://github.com/Linuxfabrik/lfops/tree/main/roles/policycoreutils): `setup_librenms__skip_policycoreutils`
* [selinux](https://github.com/Linuxfabrik/lfops/tree/main/roles/selinux): `setup_librenms__skip_selinux`
* [python](https://github.com/Linuxfabrik/lfops/tree/main/roles/python): `librenms__skip_python`
* [kernel_settings](https://github.com/Linuxfabrik/lfops/tree/main/roles/kernel_settings): `librenms__skip_kernel_settings`
* [mariadb_server](https://github.com/Linuxfabrik/lfops/tree/main/roles/mariadb_server): `librenms__skip_mariadb_server`
* [repo_remi](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_remi): `librenms__skip_repo_remi`
* [php](https://github.com/Linuxfabrik/lfops/tree/main/roles/php): `librenms__skip_php`
* [apps](https://github.com/Linuxfabrik/lfops/tree/main/roles/apps): `librenms__skip_apps`
* [librenms](https://github.com/Linuxfabrik/lfops/tree/main/roles/librenms)
* [apache_httpd](https://github.com/Linuxfabrik/lfops/tree/main/roles/apache_httpd): `librenms__skip_apache_httpd`


## setup_mastodon.yml

Calls the following roles (in order):

* [python](https://github.com/Linuxfabrik/lfops/tree/main/roles/python): `setup_mastodon__skip_python`
* [repo_postgresql](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_postgresql): `setup_mastodon__skip_repo_postgresql`
* [postgresql_server](https://github.com/Linuxfabrik/lfops/tree/main/roles/postgresql_server): `setup_mastodon__skip_postgresql_server`
* [kernel_settings](https://github.com/Linuxfabrik/lfops/tree/main/roles/kernel_settings): `setup_mastodon__skip_kernel_settings`
* [repo_remi](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_remi): `setup_mastodon__skip_repo_remi`
* [repo_redis](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_redis)
* [redis](https://github.com/Linuxfabrik/lfops/tree/main/roles/redis): `setup_mastodon__skip_redis`
* [repo_elasticsearch](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_elasticsearch): `setup_mastodon__skip_repo_elasticsearch`
* [elasticsearch](https://github.com/Linuxfabrik/lfops/tree/main/roles/elasticsearch): `setup_mastodon__skip_elasticsearch`
* [login](https://github.com/Linuxfabrik/lfops/tree/main/roles/login): `setup_mastodon__skip_login`
* [repo_baseos](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_baseos): `setup_mastodon__skip_repo_baseos`
* [repo_epel](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_epel): `setup_mastodon__skip_repo_epel`
* [policycoreutils](https://github.com/Linuxfabrik/lfops/tree/main/roles/policycoreutils): `setup_mastodon__skip_policycoreutils`
* [selinux](https://github.com/Linuxfabrik/lfops/tree/main/roles/selinux): `setup_mastodon__skip_selinux`
* [apache_httpd](https://github.com/Linuxfabrik/lfops/tree/main/roles/apache_httpd): `setup_mastodon__skip_apache_httpd`
* [mastodon](https://github.com/Linuxfabrik/lfops/tree/main/roles/mastodon)


## setup_moodle.yml

Calls the following roles (in order):

* [policycoreutils](https://github.com/Linuxfabrik/lfops/tree/main/roles/policycoreutils): `setup_moodle__skip_policycoreutils`
* [kernel_settings](https://github.com/Linuxfabrik/lfops/tree/main/roles/kernel_settings): `setup_moodle__skip_kernel_settings`
* [python](https://github.com/Linuxfabrik/lfops/tree/main/roles/python): `setup_moodle__skip_python`
* [apps](https://github.com/Linuxfabrik/lfops/tree/main/roles/apps): `setup_moodle__skip_apps`
* [repo_remi](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_remi): `setup_moodle__skip_repo_remi`
* [php](https://github.com/Linuxfabrik/lfops/tree/main/roles/php): `setup_moodle__skip_php`
* [redis](https://github.com/Linuxfabrik/lfops/tree/main/roles/redis): `setup_moodle__skip_redis`
* [repo_mydumper](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_mydumper): `setup_moodle__skip_repo_mydumper`
* [repo_mariadb](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_mariadb): `setup_moodle__skip_repo_mariadb`
* [mariadb_server](https://github.com/Linuxfabrik/lfops/tree/main/roles/mariadb_server): `setup_moodle__skip_mariadb_server`
* [apache_httpd](https://github.com/Linuxfabrik/lfops/tree/main/roles/apache_httpd): `setup_moodle__skip_apache_httpd`
* [selinux](https://github.com/Linuxfabrik/lfops/tree/main/roles/selinux): `setup_moodle__skip_selinux`
* [moodle](https://github.com/Linuxfabrik/lfops/tree/main/roles/moodle)


## setup_nextcloud.yml

Calls the following roles (in order):

* [yum_utils](https://github.com/Linuxfabrik/lfops/tree/main/roles/yum_utils): `setup_nextcloud__skip_yum_utils`
* [repo_baseos](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_baseos): `setup_nextcloud__skip_repo_baseos`
* [repo_epel](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_epel): `setup_nextcloud__skip_repo_epel`
* [policycoreutils](https://github.com/Linuxfabrik/lfops/tree/main/roles/policycoreutils): `setup_nextcloud__skip_policycoreutils`
* [python](https://github.com/Linuxfabrik/lfops/tree/main/roles/python): `setup_nextcloud__skip_python`
* [fail2ban](https://github.com/Linuxfabrik/lfops/tree/main/roles/fail2ban): `setup_nextcloud__skip_fail2ban`
* [kernel_settings](https://github.com/Linuxfabrik/lfops/tree/main/roles/kernel_settings): `setup_nextcloud__skip_kernel_settings`
* [apache_httpd](https://github.com/Linuxfabrik/lfops/tree/main/roles/apache_httpd): `setup_nextcloud__skip_apache_httpd`
* [repo_remi](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_remi): `setup_nextcloud__skip_repo_remi`
* [php](https://github.com/Linuxfabrik/lfops/tree/main/roles/php): `setup_nextcloud__skip_php`
* [repo_mydumper](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_mydumper): `setup_nextcloud__skip_repo_mydumper`
* [repo_mariadb](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_mariadb): `setup_nextcloud__skip_repo_mariadb`
* [mariadb_server](https://github.com/Linuxfabrik/lfops/tree/main/roles/mariadb_server): `setup_nextcloud__skip_mariadb_server`
* [redis](https://github.com/Linuxfabrik/lfops/tree/main/roles/redis): `setup_nextcloud__skip_redis`
* [selinux](https://github.com/Linuxfabrik/lfops/tree/main/roles/selinux): `setup_nextcloud__skip_selinux`
* [systemd_unit](https://github.com/Linuxfabrik/lfops/tree/main/roles/systemd_unit): `nextcloud__skip_systemd_unit`
* [nextcloud](https://github.com/Linuxfabrik/lfops/tree/main/roles/nextcloud)
* [repo_collabora_code](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_collabora_code): `setup_nextcloud__skip_repo_collabora_code`
* [repo_collabora](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_collabora): `setup_nextcloud__skip_repo_collabora` (default: `true`), `setup_nextcloud__skip_repo_collabora_code`
* [collabora](https://github.com/Linuxfabrik/lfops/tree/main/roles/collabora): `setup_nextcloud__skip_collabora`
* [coturn](https://github.com/Linuxfabrik/lfops/tree/main/roles/coturn): `setup_nextcloud__skip_coturn`
* [minio_client](https://github.com/Linuxfabrik/lfops/tree/main/roles/minio_client): `setup_nextcloud__skip_minio_client`
* [objectstore_backup](https://github.com/Linuxfabrik/lfops/tree/main/roles/objectstore_backup): `setup_nextcloud__skip_objectstore_backup`
* [icinga2_agent](https://github.com/Linuxfabrik/lfops/tree/main/roles/icinga2_agent)


## setup_rocketchat.yml

Calls the following roles (in order):

* [kernel_settings](https://github.com/Linuxfabrik/lfops/tree/main/roles/kernel_settings): `setup_rocketchat__skip_kernel_settings`
* [repo_baseos](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_baseos): `setup_rocketchat__skip_repo_baseos`
* [repo_epel](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_epel): `setup_rocketchat__skip_repo_epel`
* [python_venv](https://github.com/Linuxfabrik/lfops/tree/main/roles/python_venv): `setup_rocketchat__skip_python_venv`
* [repo_mongodb](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_mongodb): `setup_rocketchat__skip_repo_mongodb`
* [mongodb](https://github.com/Linuxfabrik/lfops/tree/main/roles/mongodb): `setup_rocketchat__skip_mongodb`
* [login](https://github.com/Linuxfabrik/lfops/tree/main/roles/login): `setup_rocketchat__skip_login`
* [rocketchat](https://github.com/Linuxfabrik/lfops/tree/main/roles/rocketchat)
* [podman_containers](https://github.com/Linuxfabrik/lfops/tree/main/roles/podman_containers): `setup_rocketchat__skip_podman_containers`


## setup_wordpress.yml

Calls the following roles (in order):

* [yum_utils](https://github.com/Linuxfabrik/lfops/tree/main/roles/yum_utils): `setup_wordpress__skip_yum_utils`
* [repo_baseos](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_baseos): `setup_wordpress__skip_repo_baseos`
* [repo_epel](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_epel): `setup_wordpress__skip_repo_epel`
* [repo_mydumper](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_mydumper): `setup_wordpress__skip_repo_mydumper`
* [repo_mariadb](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_mariadb): `setup_wordpress__skip_repo_mariadb`
* [policycoreutils](https://github.com/Linuxfabrik/lfops/tree/main/roles/policycoreutils): `setup_wordpress__skip_policycoreutils`
* [python](https://github.com/Linuxfabrik/lfops/tree/main/roles/python): `setup_wordpress__skip_python`
* [kernel_settings](https://github.com/Linuxfabrik/lfops/tree/main/roles/kernel_settings): `setup_wordpress__skip_kernel_settings`
* [mariadb_server](https://github.com/Linuxfabrik/lfops/tree/main/roles/mariadb_server): `setup_wordpress__skip_mariadb_server`
* [repo_remi](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_remi): `setup_wordpress__skip_repo_remi`
* [php](https://github.com/Linuxfabrik/lfops/tree/main/roles/php): `setup_wordpress__skip_php`
* [apache_httpd](https://github.com/Linuxfabrik/lfops/tree/main/roles/apache_httpd): `setup_wordpress__skip_apache_httpd`
* [selinux](https://github.com/Linuxfabrik/lfops/tree/main/roles/selinux): `setup_wordpress__skip_selinux`
* [wordpress](https://github.com/Linuxfabrik/lfops/tree/main/roles/wordpress)


## shell.yml

Calls the following roles (in order):

* [shell](https://github.com/Linuxfabrik/lfops/tree/main/roles/shell)


## snmp.yml

Calls the following roles (in order):

* [snmp](https://github.com/Linuxfabrik/lfops/tree/main/roles/snmp)


## squid.yml

Calls the following roles (in order):

* [squid](https://github.com/Linuxfabrik/lfops/tree/main/roles/squid)


## sshd.yml

Calls the following roles (in order):

* [policycoreutils](https://github.com/Linuxfabrik/lfops/tree/main/roles/policycoreutils)
* [sshd](https://github.com/Linuxfabrik/lfops/tree/main/roles/sshd)


## system_update.yml

Calls the following roles (in order):

* [yum_utils](https://github.com/Linuxfabrik/lfops/tree/main/roles/yum_utils): `system_update__skip_yum_utils`
* [at](https://github.com/Linuxfabrik/lfops/tree/main/roles/at)
* [mailx](https://github.com/Linuxfabrik/lfops/tree/main/roles/mailx)
* [postfix](https://github.com/Linuxfabrik/lfops/tree/main/roles/postfix): `system_update__skip_postfix`
* [mailto_root](https://github.com/Linuxfabrik/lfops/tree/main/roles/mailto_root): `system_update__skip_mailto_root`
* [system_update](https://github.com/Linuxfabrik/lfops/tree/main/roles/system_update)


## systemd_journald.yml

Calls the following roles (in order):

* [systemd_journald](https://github.com/Linuxfabrik/lfops/tree/main/roles/systemd_journald)


## systemd_unit.yml

Calls the following roles (in order):

* [systemd_unit](https://github.com/Linuxfabrik/lfops/tree/main/roles/systemd_unit)


## telegraf.yml

Calls the following roles (in order):

* [repo_influxdb](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_influxdb): `telegraf__skip_repo_influxdb`
* [telegraf](https://github.com/Linuxfabrik/lfops/tree/main/roles/telegraf)


## timezone.yml

Calls the following roles (in order):

* [timezone](https://github.com/Linuxfabrik/lfops/tree/main/roles/timezone)


## tools.yml

Calls the following roles (in order):

* [repo_baseos](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_baseos): `tools__skip_repo_baseos`
* [repo_epel](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_epel)
* [tools](https://github.com/Linuxfabrik/lfops/tree/main/roles/tools)


## unattended_upgrades.yml

Calls the following roles (in order):

* [unattended_upgrades](https://github.com/Linuxfabrik/lfops/tree/main/roles/unattended_upgrades)


## vsftpd.yml

Calls the following roles (in order):

* [vsftpd](https://github.com/Linuxfabrik/lfops/tree/main/roles/vsftpd)


## yum_utils.yml

Calls the following roles (in order):

* [yum_utils](https://github.com/Linuxfabrik/lfops/tree/main/roles/yum_utils)
