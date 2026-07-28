# Ansible Role linuxfabrik.lfops.rocketchat

This role installs and configures [Rocket.Chat](https://www.rocket.chat/), an Open-Source Chat system, as a Podman container.


*Available since LFOps `2.0.0`.*


## Dependent Roles

Any [LFOps playbook](https://github.com/Linuxfabrik/lfops/blob/main/playbooks/README.md) that installs this role runs these for you. Optional ones can be disabled via the playbook's skip variables.

* On RHEL-compatible systems, the EPEL repository must be enabled (role: [linuxfabrik.lfops.repo_epel](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_epel)).
* The MongoDB repository must be enabled (role: [linuxfabrik.lfops.repo_mongodb](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_mongodb)).
* MongoDB must be installed and a replica set configured (role: [linuxfabrik.lfops.mongodb](https://github.com/Linuxfabrik/lfops/tree/main/roles/mongodb)).
* A MongoDB user for Rocket.Chat must be created. Mandatory when authentication in MongoDB is enabled (role: [linuxfabrik.lfops.mongodb](https://github.com/Linuxfabrik/lfops/tree/main/roles/mongodb)).


## Requirements

Manual steps:

* Optional: set `Storage=presistent` in `/etc/systemd/journald.conf` to allow the user to use `journalctl --user` by running the [systemd_journald](https://github.com/Linuxfabrik/lfops/blob/main/playbooks/systemd_journald.yml) playbook (role: [linuxfabrik.lfops.systemd_journald](https://github.com/Linuxfabrik/lfops/tree/main/roles/systemd_journald)).
* Optional: if the host should act as a Postfix MTA, make it listen on the IP address so that the container can reach it by running the [postfix](https://github.com/Linuxfabrik/lfops/blob/main/playbooks/postfix.yml) playbook (role: [linuxfabrik.lfops.postfix](https://github.com/Linuxfabrik/lfops/tree/main/roles/postfix)).
* Make sure the container can access the MongoDB instance:
```yaml
mongodb__conf_net_bind_ip:
  - 'localhost'
  - 'fqdn.example.com' # allow access from container. make sure the DNS entry (or /etc/hosts) points to the correct ip (not 127.)
mongodb__repl_set_members:
  - 'fqdn.example.com' # else the client gets redirected to localhost, which does not work from inside the container
```


## Tags

`rocketchat`

* Installs and configure Rocket.Chat.
* Triggers: `systemctl --user restart rocketchat-container.service`.


## Mandatory Role Variables

`rocketchat__mongodb_login`

* The user account for accessing the MongoDB database. Mandatory when authentication in MongoDB is enabled.
* Type: Dictionary.

`rocketchat__root_url`

* The URL on which the Rocket.Chat server will be available.
* Type: String.

Example:

```yaml
# mandatory
rocketchat__mongodb_login:
  username: 'rocketchat'
  password: 'linuxfabrik'
rocketchat__root_url: 'https://rocketchat.example.com'
```


## Optional Role Variables

`rocketchat__container_enabled`

* Enables or disables the service, analogous to `systemctl enable/disable`.
* Type: Bool.
* Default: `true`

`rocketchat__container_state`

* Changes the state of the service, analogous to `systemctl start/stop/restart/reload`. Possible options: `started`, `stopped`, `restarted`, `reloaded`.
* Type: String.
* Default: `'started'`

`rocketchat__mongodb_host`

* The host on which MongoDB is reachable.
* Type: String.
* Default: `'host.containers.internal'`

`rocketchat__mongodb_port`

* The port on which MongoDB is reachable.
* Type: Number.
* Default: `27017`

`rocketchat__mongodb_repl_set_name`

* The name of the MongoDB replica set for Rocket.Chat.
* Type: String.
* Default: `'rs01'`

`rocketchat__port`

* The port on which Rocket.Chat server will be available.
* Type: Number.
* Default: `3000`

`rocketchat__user_home_directory`

* The home directory of the user running Rocket.Chat.
* Type: String.
* Default: `'/opt/rocketchat'`

`rocketchat__version`

* Which Rocket.Chat version to install. Have a look at the available [releases](https://github.com/RocketChat/Rocket.Chat/releases).
* Type: String.
* Default: `'latest'`

Example:

```yaml
# optional
rocketchat__container_enabled: true
rocketchat__container_state: 'started'
rocketchat__mongodb_host: 'localhost'
rocketchat__mongodb_port: 27017
rocketchat__mongodb_repl_set_name: 'rs01'
rocketchat__port: 3000
rocketchat__user_home_directory: /opt/Rocket.Chat
rocketchat__version: 'latest'
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
