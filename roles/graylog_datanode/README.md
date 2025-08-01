# Ansible Role linuxfabrik.lfops.graylog_datanode

This role installs and configures a [Graylog](https://www.graylog.org) Data Node.

Note that this role does NOT let you specify a particular Graylog Data Node version. It simply installs the latest available Graylog Data Node version from the repos configured in the system.


## Known Limitations

* To secure your data node(s), you can either upload an existing Certificate Authority (CA) or provision a certificate directly from the Graylog interface. This role does not currently support certificate handling - it assumes that you are using the automatic data node setup.
* This role does not currently support more than one data node.


## Mandatory Requirements

Sizing of disks:

* `/`: at least 4 GB free disk space (create a 8+ GB partition).
* `/var`: at least 15 GB free disk space (create a 20+ GB partition).

If you use the ["Setup Graylog Data Node" Playbook](https://github.com/Linuxfabrik/lfops/blob/main/playbooks/setup_graylog_datanode.yml), the following is automatically done for you:

* Install MongoDB. This can be done using the [linuxfabrik.lfops.mongodb](https://github.com/Linuxfabrik/lfops/tree/main/roles/mongodb) role.
* If you're not using a versioned MongoDB repository, don't forget to protect MongoDB from being updated with newer minor and major versions. This can be done using the [linuxfabrik.lfops.dnf_versionlock](https://github.com/Linuxfabrik/lfops/tree/main/roles/dnf_versionlock) role.
* Enable the official [Graylog repository](https://go2docs.graylog.org/current/downloading_and_installing_graylog/red_hat_installation.htm). This can be done using the [linuxfabrik.lfops.repo_graylog](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_graylog) role.


## Tags

| Tag                           | What it does                                    |
| ---                           | ------------                                    |
| `graylog_datanode`            | Installs and configures Graylog Data Node          |
| `graylog_datanode:configure`  | Deploys the config files |
| `graylog_datanode:state`      | Manages the state of the Graylog Data Node service |


## Mandatory Role Variables

| Variable | Description |
| -------- | ----------- |
| `graylog_datanode__password_secret` | String. You MUST set a secret that is used for password encryption and salting. The server refuses to start if this value is not set. The minimum length for `password_secret` is 16 characters. Use at least 64 characters. If you run multiple Graylog Data Nodes, make sure you use the same password_secret for all of them. |

Example:
```yaml
# mandatory
graylog_datanode__password_secret: 'Linuxfabrik_GmbH'
```


## Optional Role Variables

| Variable | Description | Default Value |
| -------- | ----------- | ------------- |
| `graylog_datanode__bind_address` | String. The network interface used by the Graylog DataNode to bind all services. | `'127.0.0.1'` |
| `graylog_datanode__http_port`    | Number. The port where the DataNode REST api is listening. | `8999` |
| `graylog_datanode__mongodb_uri`  | String. MongoDB connection string. See https://docs.mongodb.com/manual/reference/connection-string/ for details. | `'mongodb://127.0.0.1/graylog'` |
| `graylog_datanode__opensearch_data_location` | String. Set this OpenSearch folder if you need OpenSearch to be located in a special place. | `/var/lib/graylog-datanode/opensearch/data` |

Example:
```yaml
# optional
graylog_datanode__bind_address: '127.0.0.1'
graylog_datanode__datanode_http_port: 8999
graylog_datanode__mongodb_uri: 'mongodb://127.0.0.1/graylog'
graylog_datanode__opensearch_data_location: '/data/opensearch'
```


## Troubleshooting

Q: `/bin/sh: /opt/python-venv/pymongo/bin/python3: No such file or directory`

A: You either have to run the whole playbook, or python_venv directly: `ansible-playbook --inventory myinv linuxfabrik.lfops.setup_graylog_datanode --tags python_venv`


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
