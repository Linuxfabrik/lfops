# Ansible Role linuxfabrik.lfops.proxysql

This role installs and configures [ProxySQL](https://proxysql.com/). Note that running this role always reloads the config from `/etc/proxysql.cnf` into ProxySQL's internal database.


## Tags

`proxysql`

* Installs and configures ProxySQL.
* Triggers: proxysql-initial.service restart.

`proxysql:configure`

* Manages the config file.
* Triggers: proxysql-initial.service restart.

`proxysql:state`

* Manages the state of the systemd service.
* Triggers: none.


## Mandatory Role Variables

`proxysql__admin_users`

* The ProxySQL account for administrating ProxySQL.
* Type: List of dictionaries.

`proxysql__monitor_users`

* The MariaDB account for monitoring the backend SQL nodes. The user has to exist in MariaDB and have `USAGE, REPLICATION CLIENT,REPLICA MONITOR` privileges.
* Type: Dictionary.

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

`proxysql__cluster_user`

* Account used internally for communication in ProxySQL clusters.
* Type: Dictionary.
* Default: unset

`proxysql__mysql_galera_hostgroups__host_var` / `proxysql__mysql_galera_hostgroups__group_var`

* List of dictionaries defining the hostgroups for the use with Galera.
* For the usage in `host_vars` / `group_vars` (can only be used in one group at a time).
* Type: List of dictionaries.
* Default: `[]`
* Subkeys:

    * `*_hostgroup`:

        * Mandatory. ID of the respective hostgroup.
        * Type: Number.

    * `max_writers`:

        * Optional. Maximum number of nodes that should be allowed in the `writer_hostgroup`, nodes in excess of this value will be put into the `backup_writer_hostgroup`.
        * Type: Number.
        * Default: `1`

    * `writer_is_also_reader`:

        * Optional. Determines if a node should be added to the `reader_hostgroup` as well as the `writer_hostgroup`. Value of `2` signals that only the nodes in `backup_writer_hostgroup` are also in `reader_hostgroup`, excluding the node(s) in the `writer_hostgroup`.
        * Type: Number.
        * Default: `0`

    * `max_transactions_behind`:

        * Optional. Maximum number of writesets behind the cluster that ProxySQL should allow before shunning the node to prevent stale reads.
        * Type: Number.
        * Default: `0`

    * `state`:

        * Optional. State, either `present` or `absent`.
        * Type: String.
        * Default: `present`

`proxysql__mysql_query_rules__host_var` / `proxysql__mysql_query_rules__group_var`

* List of dictionaries determining the routing of queries to the backends.
* For the usage in `host_vars` / `group_vars` (can only be used in one group at a time).
* Type: List of dictionaries.
* Default: `[]`
* Subkeys:

    * `rule_id`:

        * Mandatory. Unique ID of the rule. Rules are processed in `rule_id` order.
        * Type: Number.

    * `match_pattern`:

        * Mandatory. Regular expression that matches the query text.
        * Type: String.

    * `destination_hostgroup`:

        * Mandatory. ID of the hostgroup to which the query gets routed.
        * Type: Number.

    * `active`:

        * Optional. State of the rule.
        * Type: Bool.

    * `apply`:

        * Optional. When set to `true` no further queries will be evaluated after this rule is matched and processed.
        * Type: Bool.

    * `state`:

        * Optional. State, either `present` or `absent`.
        * Type: String.
        * Default: `present`

`proxysql__mysql_replication_hostgroups__host_var` / `proxysql__mysql_replication_hostgroups__group_var`

* List of dictionaries defining the hostgroups for the use with MariaDB/MySQL replication.
* For the usage in `host_vars` / `group_vars` (can only be used in one group at a time).
* Type: List of dictionaries.
* Default: `[]`
* Subkeys:

    * `*_hostgroup`:

        * Mandatory. ID of the respective hostgroup.
        * Type: Number.

    * `state`:

        * Optional. State, either `present` or `absent`.
        * Type: String.
        * Default: `present`

`proxysql__mysql_servers__host_var` / `proxysql__mysql_servers__group_var`

* List of dictionaries defining the backend MariaDB/MySQL servers.
* For the usage in `host_vars` / `group_vars` (can only be used in one group at a time).
* Type: List of dictionaries.
* Default: `[]`
* Subkeys:

    * `address`:

        * Mandatory. Address.
        * Type: String.

    * `port`:

        * Optional. Port.
        * Type: Number.
        * Default: `3306`

    * `use_ssl`:

        * Optional. Determines if SSL is used for the connection to the backend.
        * Type: Bool.
        * Default: `false`

    * `weight`:

        * Optional. Determines the priority of the backend.
        * Type: Number.
        * Default: `1`

    * `max_replication_lag`:

        * Optional. If greater than 0, ProxySQL will regularly monitor replication lag and if it goes beyond the configured threshold it will temporary shun the host until replication catches up.
        * Type: Number.
        * Default: `0`

    * `state`:

        * Optional. State, either `present` or `absent`.
        * Type: String.
        * Default: `present`

`proxysql__mysql_users__host_var` / `proxysql__mysql_users__group_var`

* List of dictionaries defining the MariaDB/MySQL users. They have to already exist in the DB.
* For the usage in `host_vars` / `group_vars` (can only be used in one group at a time).
* Type: List of dictionaries.
* Default: `[]`
* Subkeys:

    * `username`:

        * Mandatory. Username.
        * Type: String.

    * `password`:

        * Optional. Port.
        * Type: Number.
        * Default: `3306`

    * `use_ssl`:

        * Optional. Determines if SSL is used for the connection to the backend.
        * Type: Bool.
        * Default: `false`

    * `default_hostgroup`:

        * Optional. If there is no matching rule for the queries sent by this user, the traffic it generates is sent to the specified hostgroup.
        * Type: Number.
        * Default: `0`

    * `state`:

        * Optional. State, either `present` or `absent`.
        * Type: String.
        * Default: `present`

`proxysql__proxysql_servers__host_var` / `proxysql__proxysql_servers__group_var`

* List of dictionaries defining the ProxySQL inside a cluster.
* For the usage in `host_vars` / `group_vars` (can only be used in one group at a time).
* Type: List of dictionaries.
* Default: `[]`
* Subkeys:

    * `hostnaem`:

        * Mandatory. Hostname / Address.
        * Type: String.

    * `port`:

        * Optional. Port.
        * Type: Number.
        * Default: `6032`

    * `state`:

        * Optional. State, either `present` or `absent`.
        * Type: String.
        * Default: `present`

`proxysql__service_enabled`

* Enables or disables the ProxySQL service, analogous to `systemctl enable/disable --now`.
* Type: Bool.
* Default: `true`

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
