# Ansible Role linuxfabrik.lfops.rocketchat

This role installs and configures [Rocket.Chat](https://www.rocket.chat/), an Open-Source Chat system, as a Podman container.


## Mandatory Requirements

* On RHEL-compatible systems, enable the EPEL repository. This can be done using the [linuxfabrik.lfops.repo_epel](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_epel) role.
* Enable the MongoDB repository. This can be done using the [linuxfabrik.lfops.repo_mongodb](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_mongodb) role.
* Install MongoDB and configure a replica set. This can be done using the [linuxfabrik.lfops.mongodb](https://github.com/Linuxfabrik/lfops/tree/main/roles/mongodb) role.
* Create a MongoDB user for Rocket.Chat. Mandatory when authentication in MongoDB is enabled. This can be done using the [linuxfabrik.lfops.mongodb](https://github.com/Linuxfabrik/lfops/tree/main/roles/mongodb) role.

If you use the ["Setup Rocket.Chat" Playbook](https://github.com/Linuxfabrik/lfops/blob/main/playbooks/setup_rocketchat.yml), this is automatically done for you (you still have to take care of providing the required versions).

* Make sure the container can access the MongoDB instance:
```yaml
mongodb__conf_net_bind_ip:
  - 'localhost'
  - 'fqdn.example.com' # allow access from container. make sure the DNS entry (or /etc/hosts) points to the correct ip (not 127.)
mongodb__repl_set_members:
  - 'fqdn.example.com' # else the client gets redirected to localhost, which does not work from inside the container
```


## Optional Requirements

* It is recommended to set `Storage=presistent` in `/etc/systemd/journald.conf` to allow the user to use `journalctl --user`. This can be done using the [linuxfabrik.lfops.systemd_journald](https://github.com/Linuxfabrik/lfops/tree/main/roles/systemd_journald) role.
* If the host should act as a Postfix MTA, make sure it is listening on the IP address so that the container can reach it. This can be done using the [linuxfabrik.lfops.systemd_journald](https://github.com/Linuxfabrik/lfops/tree/main/roles/systemd_journald) role.


## Tags

| Tag          | What it does                       |
| ---          | ------------                       |
| `rocketchat` | Installs and configure Rocket.Chat |


## Mandatory Role Variables
| Variable                  | Description                                                |
| --------                  | -----------                                                |
| `rocketchat__mongodb_login` | The user account for accessing the MongoDB database. Mandatory when authentication in MongoDB is enabled. |
| `rocketchat__root_url`    | The URL on which the Rocket.Chat server will be available. |

Example:
```yaml
# mandatory
rocketchat__mongodb_login:
  username: 'rocketchat'
  password: 'linuxfabrik'
rocketchat__root_url: 'https://rocketchat.example.com'
```


## Optional Role Variables

| Variable | Description | Default Value |
| -------- | ----------- | ------------- |
| `rocketchat__container_enabled`| Enables or disables the service, analogous to `systemctl enable/disable`. | `true` |
| `rocketchat__container_state` | Changes the state of the service, analogous to `systemctl start/stop/restart/reload`. Possible options:<br> * `started`<br> * `stopped`<br> * `restarted`<br> * `reloaded` | `'started'` |
| `rocketchat__mongodb_host`| The host on which MongoDB is reachable. | `'host.containers.internal'` |
| `rocketchat__mongodb_port`| The port on which MongoDB is reachable. | `27017` |
| `rocketchat__mongodb_repl_set_name`| The name of the MongoDB replica set for Rocket.Chat. | `'rs01'` |
| `rocketchat__port`| The port on which Rocket.Chat server will be available. | `3000` |
| `rocketchat__user_home_directory`| The home directory of the user running Rocket.Chat. | `/opt/rocketchat` |
| `rocketchat__version`| Which Rocket.Chat version to install. Have a at the available [releases](https://github.com/RocketChat/Rocket.Chat/releases). | `'latest'` |

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
