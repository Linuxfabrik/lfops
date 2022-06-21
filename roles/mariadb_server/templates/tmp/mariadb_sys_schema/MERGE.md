# Merging from MySQL sys schema

MariaDB up to 10.4 contains a MySQL 5.6 `PERFORMANCE_SCHEMA` (P_S):

    SQL> SELECT @@version, plugin_name, plugin_auth_version
      FROM information_schema.plugins
     WHERE plugin_name = 'PERFORMANCE_SCHEMA'
    ;
    +--------------------+--------------------+---------------------+
    | @@version          | plugin_name        | plugin_auth_version |
    +--------------------+--------------------+---------------------+
    | 10.4.6-MariaDB-log | PERFORMANCE_SCHEMA | 5.6.40              |
    +--------------------+--------------------+---------------------+

MySQL 5.6 P_S is not available in the MySQL downloads but only here on github. Thus we have branched this project from mysql/mysql-sys.

MySQL 5.7 and newer is available in the MySQL downloads under `share/mysql_sys_schema.sql`. So we could merge from there.

## Further tasks

* Backport as much as possible from MySQL 5.7 and MySQL 8.0 sys schema to MariaDB sys schema.
* Merge changes from other sources, see below.

The `sys` schema version can be found as follows:

    SQL> SELECT * FROM sys.version;
    +-------------+---------------+
    | sys_version | mysql_version |
    +-------------+---------------+
    | 1.5.1       | 5.7.25-log    |
    +-------------+---------------+

In MySQL 5.7 an inline file is shipped. To generate the same file you can run:

    ./generate_sql_file.sh -v 57 -m
    diff gen/mysql_sys_schema.sql /home/mysql/product/mysql-5.7/share/mysql_sys_schema.sql 

It looks like our current mysql_sys_schema.sql is the same as original MySQL 5.7.26. So nothing has changed since then.

## Sources found in the Internet

* [bundle sys schema MDEV-9077](https://jira.mariadb.org/browse/MDEV-9077 "MDEV-9077")
* [The MariaDB sys schema](https://github.com/good-dba/mariadb-sys)
* [Compatibility for MariaDB](https://github.com/mysql/mysql-sys/pull/99)
* [The MySQL sys schema](https://github.com/jynus/mysql-sys "jynus/mysql-sys forked from mysql/mysql-sys")
* [Sys schema on MariaDB #362](https://github.com/major/MySQLTuner-perl/issues/362)
* [MySQL sys Schema in MariaDB 10.2](https://www.fromdual.com/mysql-sys-schema-in-mariadb-10-2)

## Run the test suite

I still have to figure out how this works because sys schema does not provide `mysql-test-run.pl`...

    cd mysql-test
    ./mysql-test-run.pl .
