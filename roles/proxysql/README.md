# Ansible Role linuxfabrik.lfops.proxysql

This role installs and configures [ProxySQL](https://proxysql.com/). Note that running this role always reloads the config from `/etc/proxysql.cnf` into ProxySQL's internal database.


## Tags

| Tag                  | What it does                             |
| ---                  | ------------                             |
| `proxysql`           | Installs and configures ProxySQL         |
| `proxysql:configure` | Manages the config file                  |
| `proxysql:state`     | Manages the state of the systemd service |


## Mandatory Role Variables

| Variable | Description |
| -------- | ----------- |
| `proxysql__admin_users` | The ProxySQL account for administrating ProxySQL. |
| `proxysql__monitor_users` | The MariaDB account for monitoring the backend SQL nodes. The user has to exist in MariaDB and have `USAGE, REPLICATION CLIENT,REPLICA MONITOR` privileges. |

Example:
```yaml
# mandatory
proxysql__admin_users:
  - username: 'proxysql-admin'
    password: 'linuxfabrik'
proxysql__monitor_user:
  username: 'proxysql-monitor'
  password: 'linuxfabrik'
```


## Optional Role Variables

| Variable | Description | Default Value |
| -------- | ----------- | ------------- |
| `proxysql__cluster_user` | Account used internally for communication in ProxySQL clusters. | unset |
| `proxysql__mysql_galera_hostgroups__host_var` / <br> `proxysql__mysql_galera_hostgroups__group_var` | List of dictionaries defining the hostgroups for the use with Galera. Subkeys: <ul><li>`*_hostgroup`: Mandatory, int. ID of the respective hostgroup.</li><li>`max_writers`: Optional, int. Maximum number of nodes that should be allowed in the `writer_hostgroup`, nodes in excess of this value will be put into the `backup_writer_hostgroup`. Defaults to `1`.</li><li>`writer_is_also_reader`: Optional, int. Determines if a node should be added to the `reader_hostgroup` as well as the `writer_hostgroup`. Value of `2` signals that only the nodes in `backup_writer_hostgroup` are also in `reader_hostgroup`, excluding the node(s) in the `writer_hostgroup`. Defaults to `0`.</li><li>`max_transactions_behind`: Optional, int. Maximum number of writesets behind the cluster that ProxySQL should allow before shunning the node to prevent stale reads. Defaults to `0`.</li><li>`state`: Optional, string. State, either `present` or `absent`. Defaults to `present`.</li></ul> | `[]` |
| `proxysql__mysql_query_rules__host_var` / <br> `proxysql__mysql_query_rules__group_var` | List of dictionaries determining the routing of queries to the backends. Subkeys: <ul><li>`rule_id`: Mandatory, int. Unique ID of the rule. Rules are processed in `rule_id` order.</li><li>`match_pattern`: Mandatory, string. Regular expression that matches the query text.</li><li>`destination_hostgroup`: Mandatory, int. ID of the hostgroup to which the query gets routed.</li><li>`active`: Optional, boolean. State of the rule.</li><li>`apply`: Optional, boolean. When set to `true` no further queries will be evaluated after this rule is matched and processed.</li><li>`state`: Optional, string. State, either `present` or `absent`. Defaults to `present`.</li></ul> | `[]` |
| `proxysql__mysql_replication_hostgroups__host_var` / <br> `proxysql__mysql_replication_hostgroups__group_var` | List of dictionaries defining the hostgroups for the use with MariaDB/MySQL replication. Subkeys: <ul><li>`*_hostgroup`: Mandatory, int. ID of the respective hostgroup.</li><li>`state`: Optional, string. State, either `present` or `absent`. Defaults to `present`.</li></ul> | `[]` |
| `proxysql__mysql_servers__host_var` / <br> `proxysql__mysql_servers__group_var` | List of dictionaries defining the backend MariaDB/MySQL servers. Subkeys: <ul><li>`address`: Mandatory, string. Address.</li><li>`port`: Optional, int. Port. Defaults to `3306`.</li><li>`use_ssl`: Optional, boolean. Determines if SSL is used for the connection to the backend. Defaults to `false`.</li><li>`weight`: Optional, int. Determines the priority of the backend. Defaults to `1`.</li><li>`max_replication_lag`: Optional, int. If greater than 0, ProxySQL will regularly monitor replication lag and if it goes beyond the configured threshold it will temporary shun the host until replication catches up. Defaults to `0`.</li><li>`state`: Optional, string. State, either `present` or `absent`. Defaults to `present`.</li></ul> | `[]` |
| `proxysql__mysql_users__host_var` / <br> `proxysql__mysql_users__group_var` | List of dictionaries defining the MariaDB/MySQL users. They have to already exist in the DB. Subkeys: <ul><li>`username`: Mandatory, string. Username.</li><li>`password`: Optional, int. Port. Defaults to `3306`.</li><li>`use_ssl`: Optional, boolean. Determines if SSL is used for the connection to the backend. Defaults to `false`.</li><li>`default_hostgroup`: Optional, int. If there is no matching rule for the queries sent by this user, the traffic it generates is sent to the specified hostgroup. Defaults to `0`.</li><li>`state`: Optional, string. State, either `present` or `absent`. Defaults to `present`.</li></ul> | `[]` |
| `proxysql__proxysql_servers__host_var` / <br> `proxysql__proxysql_servers__group_var` | List of dictionaries defining the ProxySQL inside a cluster. Subkeys: <ul><li>`hostnaem`: Mandatory, string. Hostname / Address.</li><li>`port`: Optional, int. Port. Defaults to `6032`.</li><li>`state`: Optional, string. State, either `present` or `absent`. Defaults to `present`.</li></ul> | `[]` |
| `proxysql__service_enabled` | Enables or disables the ProxySQL service, analogous to `systemctl enable/disable --now`. | `true` |

Example:
```yaml
# optional
proxysql__cluster_user:
  username: 'proxysql-monitor'
  password: 'linuxfabrik'
proxysql__mysql_galera_hostgroups__host_var:
  - writer_hostgroup: 0
    backup_writer_hostgroup: 3
    reader_hostgroup: 1
    offline_hostgroup: 4
    max_writers: 1
    writer_is_also_reader: 1
    max_transactions_behind: 30
proxysql__mysql_query_rules__host_var:
  # read/write split
  - rule_id: 100
    active: true
    match_pattern: '^SELECT .* FOR UPDATE'
    destination_hostgroup: 0 # writer_hostgroup
    apply: 1
  - rule_id: 200
    active: true
    match_pattern: '^SELECT .*'
    destination_hostgroup: 1 # reader_hostgroup
    apply: 1
  - rule_id: 300
    active: true
    match_pattern: '.*'
    destination_hostgroup: 0 # writer_hostgroup
    apply: 1
proxysql__mysql_replication_hostgroups__host_var:
  writer_hostgroup: 0
  reader_hostgroup: 1
proxysql__mysql_servers__host_var:
  - address: 'mariadb01.example.com'
    port: 3306
    use_ssl: true
    hostgroup: 10
    weight: 100
    max_replication_lag: 30
proxysql__mysql_users__host_var:
  - username: 'user1'
    password: 'linuxfabrik'
    use_ssl: true
    default_hostgroup: 0
    state: 'present'
proxysql__proxysql_servers__group_var:
  - hostname: 'proxysql1.example.com'
    port: 6032
  - hostname: 'proxysql2.example.com'
    port: 6032
proxysql__service_enabled: true
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
