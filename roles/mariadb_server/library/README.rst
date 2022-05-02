Code inspired by https://github.com/ansible-collections/community.mysql.

We had to re-implement the user part due to the erroneous of the mysql_user plugin, which creates a user once, but always fails updating an existing one.

Our version is kept as simple as possible (so just username/password auth is supported, nothing fancy). We NEED a DBA user with a password.

Updating a user in MariaDB always means:

* DROP user
* CREATE user
* GRANT privileges

So no need to "append_privs", but of course this always leads to a "changed".

Using MariaDB 10.1.3 onwards, a ``CREATE OR REPLACE USER IF NOT EXISTS foo2@test IDENTIFIED BY 'password';`` would simplify this, but MariaDB is unable to understand ``CREATE OR REPLACE`` in combination with ``IF NOT EXISTS`` (only parts of it, see https://mariadb.com/kb/en/create-user/).
