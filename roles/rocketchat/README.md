# Ansible Role linuxfabrik.lfops.rocketchat

This role installs and configures [Rocket.Chat](https://www.rocket.chat/), an Open-Source Chat system.


## Mandatory Requirements

* On RHEL-compatible systems, enable the EPEL repository. This can be done using the [linuxfabrik.lfops.repo_epel](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_epel) role.
* Install git. This can be done using the [linuxfabrik.lfops.git](https://github.com/Linuxfabrik/lfops/tree/main/roles/git) role.
* Install nodejs. This can be done using the [linuxfabrik.lfops.nodejs](https://github.com/Linuxfabrik/lfops/tree/main/roles/nodejs) role.
* Enable the MongoDB repository. This can be done using the [linuxfabrik.lfops.repo_mongodb](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_mongodb) role.
* Install MongoDB and configure a replica set. This can be done using the [linuxfabrik.lfops.mongodb](https://github.com/Linuxfabrik/lfops/tree/main/roles/mongodb) role.
* Create a MongoDB user for Rocket.Chat. Mandatory when authentication in MongoDB is enabled. This can be done using the [linuxfabrik.lfops.mongodb](https://github.com/Linuxfabrik/lfops/tree/main/roles/mongodb) role.

If you use the ["Setup Rocket.Chat" Playbook](https://github.com/Linuxfabrik/lfops/blob/main/playbooks/setup_rocketchat.yml), thinstallation is automatically done for you (you still have to take care of providing the required versions).


## Tags

| Tag                 | What it does                                 |
| ---                 | ------------                                 |
| `rocketchat`        | Installs Rocket.Chat                         |
| `rocketchat:update` | Updates Rocket.Chat to the specified version |


## Mandatory Role Variables
| Variable                  | Description                                                |
| --------                  | -----------                                                |
| `rocketchat__mongodb_login` | The user account for accessing the MongoDB database. Mandatory when authentication in MongoDB is enabled. |
| `rocketchat__npm_version` | The required NPM version for the Rocket.Chat version. Have a look at the [release page](https://github.com/RocketChat/Rocket.Chat/releases). (Sadly this value is not available via the releases.rocket.chat api). |
| `rocketchat__root_url`    | The URL on which the Rocket.Chat server will be available. |

Example:
```yaml
# mandatory
rocketchat__mongodb_login:
  username: 'rocketchat'
  password: 'linuxfabrik'
rocketchat__npm_version: '6.14.17'
rocketchat__root_url: 'https://rocketchat.example.com'
```


## Optional Role Variables

| Variable | Description | Default Value |
| -------- | ----------- | ------------- |
| `rocketchat__application_path`| The directory in which Rocket.Chat should be installed. | `/opt/Rocket.Chat` |
| `rocketchat__mongodb_host`| The host on which MongoDB is reachable. | `'localhost'` |
| `rocketchat__mongodb_port`| The port on which MongoDB is reachable. | `27017` |
| `rocketchat__mongodb_repl_set_name`| The name of the MongoDB replica set for Rocket.Chat. | `'rs01'` |
| `rocketchat__port`| The port on which Rocket.Chat server will be available. | `3000` |
| `rocketchat__service_enabled`| Enables or disables the service, analogous to `systemctl enable/disable`. | `true` |
| `rocketchat__service_state` | Changes the state of the service, analogous to `systemctl start/stop/restart/reload`. Possible options:<br> * `started`<br> * `stopped`<br> * `restarted`<br> * `reloaded` | `'started'` |
| `rocketchat__version`| Which Rocket.Chat version to install. Have a at the available [releases](https://github.com/RocketChat/Rocket.Chat/releases). | `'latest'` |

Example:
```yaml
# optional
rocketchat__application_path: /opt/Rocket.Chat
rocketchat__mongodb_host: 'localhost'
rocketchat__mongodb_port: 27017
rocketchat__mongodb_repl_set_name: 'rs01'
rocketchat__port: 3000
rocketchat__service_enabled: true
rocketchat__service_state: 'started'
# Versions according to https://github.com/RocketChat/Rocket.Chat/releases
rocketchat__version: 'latest'
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
