# Ansible Role linuxfabrik.lfops.mongodb

This role installs and configures a [MongoDB](https://www.mongodb.com/) server.

Tested on

* RHEL 8 (and compatible)


## Mandatory Requirements

* Enable the official [MongoDB repository](https://www.mongodb.com/docs/manual/tutorial/install-mongodb-on-red-hat/#install-mongodb-community-edition). This can be done using the [linuxfabrik.lfops.repo_mongodb](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_mongodb) role.


## Tags

| Tag             | What it does                            |
| ---             | ------------                            |
| `mongodb`       | Installs and configures MongoDB         |
| `mongodb:state` | Manages the state of the mongod service |


## Optional Role Variables

| Variable | Description | Default Value |
| -------- | ----------- | ------------- |
| `mongodb__conf_net_bind_ip` | The IP on which MongoDB should be available. Have a look at [mongodb.com](https://www.mongodb.com/docs/manual/reference/configuration-options/#mongodb-setting-net.bindIp). | `'127.0.0.1'` |
| `mongodb__conf_net_port` | The port on which MongoDB should be available. | `27017` |
| `mongodb__conf_replication_oplog_size_mb` | [mongodb.com](https://www.mongodb.com/docs/manual/reference/configuration-options/#mongodb-setting-replication.oplogSizeMB) | unset |
| `mongodb__conf_replication_repl_set_name` | Set this to enable replication. Have a look at <https://www.mongodb.com/docs/manual/reference/configuration-options/#mongodb-setting-replication.replSetName>. | unset |
| `mongodb__conf_security_authorization` | [mongodb.com](https://www.mongodb.com/docs/manual/reference/configuration-options/#mongodb-setting-security.authorization) | `false` |
| `mongodb__conf_storage_directory_per_db` | [mongodb.com](https://www.mongodb.com/docs/manual/reference/configuration-options/#mongodb-setting-storage.directoryPerDB) | `true` |
| `mongodb__conf_storage_engine_raw` | [mongodb.com](https://www.mongodb.com/docs/manual/reference/configuration-options/#mongodb-setting-storage.engine) | unset |
| `mongodb__conf_storage_journal_commit_interval_ms` | [mongodb.com](https://www.mongodb.com/docs/manual/reference/configuration-options/#mongodb-setting-storage.journal.commitIntervalMs) | `100` |
| `mongodb__conf_storage_journal_enabled` | Enable or disable the durability journal to ensure data files remain valid and recoverable. | `true` |

Example:
```yaml
# optional
mongodb__conf_net_bind_ip: '127.0.0.1' # https://www.mongodb.com/docs/manual/reference/configuration-options/#mongodb-setting-net.bindIp
mongodb__conf_net_port: 27017
mongodb__conf_replication_oplog_size_mb: 50
mongodb__conf_replication_repl_set_name: 'replSet1'
mongodb__conf_security_authorization: false
mongodb__conf_storage_directory_per_db: true
mongodb__conf_storage_engine_raw: |-
  engine: "wiredTiger"
    wiredTiger:
      engineConfig:
        cacheSizeGB: 1
        journalCompressor: none
        directoryForIndexes: false
      collectionConfig:
        blockCompressor: none
      indexConfig:
        prefixCompression: false
mongodb__conf_storage_journal_commit_interval_ms: 100
mongodb__conf_storage_journal_enabled: true
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
