# STIGs

Hardenings that can be covered by LFOps.


## MariaDB

Backup Policy in Place

* CIS 10.11 Benchmark - v1.0.0 - 03-29-2024 - 2.1.1

Do Not Reuse Usernames

* CIS 10.11 Benchmark - v1.0.0 - 03-29-2024 - 2.4

Enable data-at-rest encryption in MariaDB

* CIS 10.11 Benchmark - v1.0.0 - 03-29-2024 - 4.9

Ensure 'datadir' Has Appropriate Permissions

* if `mariadb_server__datadir_mode__host_var: 0o750` is set. Make sure that the socket is not inside the datadir in that case, else other users (eg apache) cannot reach it.
* CIS 10.11 Benchmark - v1.0.0 - 03-29-2024 - 3.1

Ensure 'general_log_file' Has Appropriate Permissions

* CIS 10.11 Benchmark - v1.0.0 - 03-29-2024 - 3.6

Ensure 'log_error' Has Appropriate Permissions

* CIS 10.11 Benchmark - v1.0.0 - 03-29-2024 - 3.3

Ensure 'log_error' is configured correctly

* CIS 10.11 Benchmark - v1.0.0 - 03-29-2024 - 6.1

Ensure 'server_audit_file_path' Has Appropriate Permissions

* CIS 10.11 Benchmark - v1.0.0 - 03-29-2024 - 3.9

Ensure 'slow_query_log' Has Appropriate Permissions

* CIS 10.11 Benchmark - v1.0.0 - 03-29-2024 - 3.4

Ensure 'sql_mode' Contains 'STRICT_ALL_TABLES'

* CIS 10.11 Benchmark - v1.0.0 - 03-29-2024 - 4.8

Ensure Audit Logging Is Enabled

* CIS 10.11 Benchmark - v1.0.0 - 03-29-2024 - 6.4

Ensure Binary and Relay Logs are Encrypted

* CIS 10.11 Benchmark - v1.0.0 - 03-29-2024 - 6.6

Ensure Example or Test Databases are Not Installed on Production Servers

* CIS 10.11 Benchmark - v1.0.0 - 03-29-2024 - 4.2

Ensure File Key Management Encryption Plugin files have appropriate permissions

* CIS 10.11 Benchmark - v1.0.0 - 03-29-2024 - 3.10

Ensure Interactive Login is Disabled

* CIS 10.11 Benchmark - v1.0.0 - 03-29-2024 - 1.5

Ensure MariaDB is Bound to One or More Specific IP Addresses

* CIS 10.11 Benchmark - v1.0.0 - 03-29-2024 - 2.9

Ensure MariaDB is Run Under a Sandbox Environment (package default)

* CIS 10.11 Benchmark - v1.0.0 - 03-29-2024 - 1.7

Ensure No Anonymous Accounts Exist

* CIS 10.11 Benchmark - v1.0.0 - 03-29-2024 - 7.6

Ensure the Audit Plugin Can't be Unloaded

* CIS 10.11 Benchmark - v1.0.0 - 03-29-2024 - 6.5

Limit Accepted Transport Layer Security (TLS) Versions

* CIS 10.11 Benchmark - v1.0.0 - 03-29-2024 - 2.10

Place Databases on Non-System Partitions

* CIS 10.11 Benchmark - v1.0.0 - 03-29-2024 - 1.1

Secure Backup Credentials

* CIS 10.11 Benchmark - v1.0.0 - 03-29-2024 - 2.1.3

The Backups Should be Properly Secured

* CIS 10.11 Benchmark - v1.0.0 - 03-29-2024 - 2.1.4

Use Dedicated Least Privileged Account for MariaDB Daemon/Service (package default)

* CIS 10.11 Benchmark - v1.0.0 - 03-29-2024 - 1.2
