# Ansible Role linuxfabrik.lfops.mirror

This role installs and configures [mirror](https://github.com/Linuxfabrik/mirror).


## Mandatory Requirements

* Install Python 3. This can be done using the [linuxfabrik.lfops.python](https://github.com/Linuxfabrik/lfops/tree/main/roles/python) role.
* Install `createrepo`. This can be done using the [linuxfabrik.lfops.apps](https://github.com/Linuxfabrik/lfops/tree/main/roles/apps) role.
* Install `git`. This can be done using the [linuxfabrik.lfops.apps](https://github.com/Linuxfabrik/lfops/tree/main/roles/apps) role.
* Install `yum-utils`. This can be done using the [linuxfabrik.lfops.yum_utils](https://github.com/Linuxfabrik/lfops/tree/main/roles/yum_utils) role.

If you use the [`mirror` Playbook](https://github.com/Linuxfabrik/lfops/blob/main/playbooks/mirror.yml), this is automatically done for you.


## Tags

| Tag      | What it does                   |
| ---      | ------------                   |
| `mirror` | Installs and configures mirror |
| `mirror:configure` | Deploys `/etc/mirror.yml` |


## Mandatory Role Variables

| Variable | Description |
| -------- | ----------- |
| `mirror__reposync_repos` | A list of dictionaries containing RPM-based repositories which should be mirrored. Subkeys: Have a look at the project's [README](https://github.com/Linuxfabrik/mirror/blob/main/README.md#synopsis---the-configuration-file) |

Example:
```yaml
# mandatory
mirror__reposync_repos:
  - repoid: 'appstream'
    relative_target_path: 'rocky/8/AppStream/x86_64/os/'
  - repoid: 'baseos'
    relative_target_path: 'rocky/8/BaseOS/x86_64/os/'
  - repoid: 'extras'
    relative_target_path: 'rocky/8/extras/x86_64/os/'
  - repoid: 'powertools'
    relative_target_path: 'rocky/8/PowerTools/x86_64/os/'
```


## Optional Role Variables

| Variable | Description | Default Value |
| -------- | ----------- | ------------- |
| `mirror__base_path` | Directory under which all the repos will be placed. This directory should be served by a webserver. | `'/var/www/html/reposync-repos'` |
| `mirror__timer_enabled` | Enables or disables the mirror timer, analogous to `systemctl enable/disable --now`. | `true` |
| `mirror__webserver_user` | The user under which the webserver runs. Will be used to set the correct FACL entries so that both users can access the files. | `'apache'` |

Example:
```yaml
# optional
mirror__base_path: '/var/www/html/reposync-repos'
mirror__timer_enabled: true
mirror__webserver_user: 'nginx'
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
