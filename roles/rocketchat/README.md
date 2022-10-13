# Ansible Role linuxfabrik.lfops.python_venv

This role creates and manages various [Python 3 virtual environments (venv)](https://docs.python.org/3/library/venv.html). These are placed below `/opt/python-venv/` on the target system.

Runs on

* RHEL 7 (and compatible)
* RHEL 8 (and compatible)
* Fedora 35


## Mandatory Requirements

* linuxfabrik.lfops.repo_epel
* git
* nodejs
* repo-mongodb
* mongodb


## Tags

| Tag                 | What it does                                 |
| ---                 | ------------                                 |
| `rocketchat`        | Installs Rocket.Chat                         |
| `rocketchat:update` | Updates Rocket.Chat to the specified version |


## Mandatory Role Variables
| Variable                  | Description                                                |
| --------                  | -----------                                                |
| `rocketchat__npm_version` | The required NPM version for the Rocket.Chat version. Have a look at the [release page](https://github.com/RocketChat/Rocket.Chat/releases). (Sadly this value is not available via the releases.rocket.chat api). |
| `rocketchat__root_url`    | The URL on which the Rocket.Chat server will be available. |

Example:
```yaml
# mandatory
rocketchat__npm_version: '6.14.17'
rocketchat__root_url: 'https://rocketchat.example.com'
```


## Optional Role Variables

| Variable | Description | Default Value |
| -------- | ----------- | ------------- |
| `rocketchat__application_path`| The directory in which Rocket.Chat should be installed. | `/opt/Rocket.Chat` |
| `rocketchat__mongodb_host`| The host on which MongoDB is reachable. | `'localhost'` |
| `rocketchat__mongodb_on_localhost`| Whether the MongoDB is running on the same host as Rocket.Chat. If this is not the case, you need to manually check the version compability and manually initiate the replica set. | `true` |
| `rocketchat__mongodb_port`| The port on which MongoDB is reachable. | `27017` |
| `rocketchat__mongodb_repl_set_name`| The name of the MongoDB replica set for Rocket.Chat. Will be initiated if MongoDB is running on localhost (`rocketchat__mongodb_on_localhost`). | `'rs01'` |
| `rocketchat__port`| The port on which Rocket.Chat server will be available. | `3000` |
| `rocketchat__service_enabled`| Enables or disables the service, analogous to `systemctl enable/disable`. | `true` |
| `rocketchat__service_state` | Changes the state of the service, analogous to `systemctl start/stop/restart/reload`. Possible options:<br> * `started`<br> * `stopped`<br> * `restarted`<br> * `reloaded` | `'started'` |
| `rocketchat__version`| Which Rocket.Chat version to install. Have a at the available [releases](https://github.com/RocketChat/Rocket.Chat/releases). | `'latest'` |

Example:
```yaml
# optional
rocketchat__application_path: /opt/Rocket.Chat
rocketchat__mongodb_host: 'localhost'
rocketchat__mongodb_on_localhost: true
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
