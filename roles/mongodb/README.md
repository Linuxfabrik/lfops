# Ansible Role linuxfabrik.lfops.mongodb

This role installs and configures a [MongoDB](https://www.mongodb.com/) server, and configures daily database dumps.

Runs on

* RHEL 8 (and compatible)


## Mandatory Requirements

* Enable the official [MongoDB repository](https://www.mongodb.com/docs/manual/tutorial/install-mongodb-on-red-hat/#install-mongodb-community-edition). This can be done using the [linuxfabrik.lfops.repo_mongodb](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_mongodb) role.


## Tags

| Tag             | What it does                              |
| ---             | ------------                              |
| `mongodb`       | Installs and configures MongoDB           |
| `mongodb:dump`  | Configures the database dumping (backups) |
| `mongodb:state` | Manages the state of the mongod service   |
| `mongodb:user`  | Manages the MongoDB users                 |


## Recommended Role Variables

| Variable | Description | Default Value |
| -------- | ----------- | ------------- |
| `mongodb__admin_user` | The main user account for the database administrator. Make sure to also enabled authorization using `mongodb__conf_security_authorization`. To create additional ones, use the `mongodb__users__*` variables. Subkeys:<ul><li>`username`: Username</li><li>`password`: Password</li></ul> | unset |
| `mongodb__conf_security_authorization` | [mongodb.com](https://www.mongodb.com/docs/manual/reference/configuration-options/#mongodb-setting-security.authorization) | `false` |
| `mongodb__dump_user` | The MongoDB user for dumping the database when Role-Based Access Control is enabled (`mongodb__conf_security_authorization`). Subkeys: <br> * `auth_database`: Optional, string. Database to authenticate against. Defaults to `'admin'`. <br> * `username`: Required, string. <br> * `password`: Required, string. | unset |

```yaml
# recommended
mongodb__admin_user:
  username: 'mongodb-admin'
  password: 'linuxfabrik'
mongodb__conf_security_authorization: true
mongodb__dump_user:
  username: 'mongodb-dump'
  password: 'linuxfabrik'
```


## Optional Role Variables

| Variable | Description | Default Value |
| -------- | ----------- | ------------- |
| `mongodb__conf_net_bind_ip` | The IP on which MongoDB should be available. Have a look at [mongodb.com](https://www.mongodb.com/docs/manual/reference/configuration-options/#mongodb-setting-net.bindIp). | `'127.0.0.1'` |
| `mongodb__conf_net_port` | The port on which MongoDB should be available. | `27017` |
| `mongodb__conf_replication_oplog_size_mb` | [mongodb.com](https://www.mongodb.com/docs/manual/reference/configuration-options/#mongodb-setting-replication.oplogSizeMB) | unset |
| `mongodb__conf_replication_repl_set_name__host_var` /<br> `mongodb__conf_replication_repl_set_name__group_var` | Set this to enable replication. Have a look at <https://www.mongodb.com/docs/manual/reference/configuration-options/#mongodb-setting-replication.replSetName>. Will be initiated automatically (have a look at `mongodb__repl_set_skip_init`). <br>For the usage in `host_vars` / `group_vars` (can only be used in one group at a time). | unset |
| `mongodb__conf_storage_directory_per_db` | [mongodb.com](https://www.mongodb.com/docs/manual/reference/configuration-options/#mongodb-setting-storage.directoryPerDB) | `true` |
| `mongodb__conf_storage_engine_raw` | [mongodb.com](https://www.mongodb.com/docs/manual/reference/configuration-options/#mongodb-setting-storage.engine) | unset |
| `mongodb__conf_storage_journal_commit_interval_ms` | [mongodb.com](https://www.mongodb.com/docs/manual/reference/configuration-options/#mongodb-setting-storage.journal.commitIntervalMs) | `100` |
| `mongodb__conf_storage_journal_enabled` | Enable or disable the durability journal to ensure data files remain valid and recoverable. | `true` |
| `mongodb__dump_method_file_based_backup_dir` | Where to store the file-based backup. | `'/backup/var-lib-mongo'` |
| `mongodb__dump_method_file_based` | Use this to create file based backups by locking the instance and copying `/var/lib/mongo`. This is recommended when using `mongodb__dump_method_mongodump` is too slow. | `false` |
| `mongodb__dump_method_mongodump_backup_dir` | Where to store the `mongodump`-based backup. | `'/backup/mongodb-dump'` |
| `mongodb__dump_method_mongodump` | Use `mongodump` to create database dumps. This is recommended since it allows the most flexible restores. | `true` |
| `mongodb__dump_on_calendar` | The `OnCalendar` definition for the systemd timer. Have a look at `man systemd.time(7)` for the format. | `'*-*-* 21:{{ 59 | random(start=0, seed=inventory_hostname) }}:00'` |
| `mongodb__dump_only_if_hidden` | Use this to only run the backup if the instance is hidden. This is useful in a MongoDB cluster setupp. | `false` |
| `mongodb__dump_use_oplog` | Use this to capture incoming write operations during the dump operation to ensure that the backups reflect a consistent data state. Note that this only works on cluster setups or with replica sets. | `false` |
| `mongodb__repl_set_members` | A list of the members for initiating the replica set | `['localhost:27017']` |
| `mongodb__repl_set_skip_init` | Set this to skip the initiation of the replica set. | `false` |
| `mongodb__service_enabled`| Enables or disables the service, analogous to `systemctl enable/disable`. | `true` |
| `mongodb__service_state` | Changes the state of the service, analogous to `systemctl start/stop/restart/reload`. Possible options:<br> * `started`<br> * `stopped`<br> * `restarted`<br> * `reloaded` | `'started'` |
| `mongodb__users__group_var` /<br> `mongodb__users__host_var` | List of dictionaries of users to create (this is NOT used for the first DBA user - here, use `mongodb__admin_user`). Subkeys:<ul><li>`username`: Mandatory, string. Username.<li>`password`: Mandatory, string. Password.<li>`database`: Mandatory, string. Database in which the user should be.<li>`roles`: Optional, string or list. Either name of one of the [built-in roles](https://www.mongodb.com/docs/manual/reference/built-in-roles), or list of dictionaries with `db` and `role`.</li><li>`state`: Optional, string. State of the user. Possible options: `present`, `absent`. Defaults to `present`.</ul><br> For the usage in `host_vars` / `group_vars` (can only be used in one group at a time). | `[]` |

Example:
```yaml
# optional
mongodb__conf_net_bind_ip: '127.0.0.1' # https://www.mongodb.com/docs/manual/reference/configuration-options/#mongodb-setting-net.bindIp
mongodb__conf_net_port: 27017
mongodb__conf_replication_oplog_size_mb: 50
mongodb__conf_replication_repl_set_name__host_var: 'replSet1'
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
mongodb__dump_method_file_based: false
mongodb__dump_method_file_based_backup_dir: '/backup/var-lib-mongo'
mongodb__dump_method_mongodump: true
mongodb__dump_method_mongodump_backup_dir: '/backup/mongodb-dump'
mongodb__dump_on_calendar: ''
mongodb__dump_only_if_hidden: false
mongodb__dump_use_oplog: true
mongodb__service_enabled: true
mongodb__service_state: 'started'
mongodb__repl_set_skip_init: false
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
