# Ansible Role linuxfabrik.lfops.existdb

This role installs and configures [eXist-db](https://exist-db.org/) — a native XML database — as a systemd-managed service. It is targeted at the Numishare stack but is independent of the other roles in the `setup_numishare` playbook and can be used standalone.

The role:

* Installs eXist-db from the upstream `unix.tar.bz2` release tarball into `existdb__install_dir` (default `/opt/existdb`).
* Creates the `existdb` system user and group, plus the data and log directories.
* Rewrites the shipped Jetty/log4j2 configuration so HTTP binds to `existdb__http_port` (default `8888`), HTTPS to `existdb__https_port` (default `8444`), data lives under `existdb__data_dir`, and logs under `existdb__log_dir`. Default ports are shifted off `8080`/`8443` to leave room for an application server (Tomcat, Wildfly).
* Sets the `admin` password on first install only (a marker file under the install dir prevents re-runs from overwriting a manually changed password).
* Drops a systemd unit file and starts the service.
* Optionally deploys a `mariadb-dump`-style backup pipeline (`existdb-dump.service` + `.timer`).


## Tags

`existdb`

* Installs and configures the whole eXist-db service, plus the backup units.

`existdb:backup`

* Limits the run to the backup pipeline (script, conf, service, timer).


## Mandatory Role Variables

None. All variables have defaults; the admin password defaults to `'linuxfabrik'` and **must** be overridden in the inventory for any non-throwaway install.


## Optional Role Variables

`existdb__admin_password`

* Password for the eXist-db `admin` user. Set on first install only; subsequent runs do not touch it.
* Type: String.
* Default: `'linuxfabrik'` — change this.

`existdb__data_dir`

* Where eXist-db stores its index/journal files.
* Type: String.
* Default: `'/var/lib/existdb/data'`

`existdb__group`

* System group that owns the install dir and runs the service.
* Type: String.
* Default: `'existdb'`

`existdb__http_port`

* Jetty HTTP port. Shifted off the application-server-default `8080` so eXist-db can coexist with Tomcat or Wildfly on the same host.
* Type: Number.
* Default: `8888`

`existdb__https_port`

* Jetty HTTPS port. Shifted off `8443` for the same reason.
* Type: Number.
* Default: `8444`

`existdb__install_dir`

* Where the tarball is extracted to.
* Type: String.
* Default: `'/opt/existdb'`

`existdb__java_opts`

* JVM options passed to the eXist-db service via systemd `Environment=JAVA_OPTS`.
* Type: String.
* Default: `'-XX:+UseG1GC -XX:+UseStringDeduplication -XX:MaxRAMPercentage=75.0'`

`existdb__log_dir`

* Where eXist-db's log4j2 writes log files.
* Type: String.
* Default: `'/var/log/existdb'`

`existdb__service_enabled`

* Enables or disables the service, analogous to `systemctl enable/disable --now`.
* Type: Bool.
* Default: `true`

`existdb__user`

* System user that owns the install dir and runs the service.
* Type: String.
* Default: `'existdb'`

`existdb__version`

* Upstream release version. The role downloads `https://github.com/eXist-db/exist/releases/download/eXist-{{ existdb__version }}/exist-distribution-{{ existdb__version }}-unix.tar.bz2`.
* Type: String.
* Default: `'6.4.1'`


## Backup and Restore

The role can deploy a `mariadb-dump`-style backup pipeline. On every run the dumper wipes `existdb__dump_directory` and writes a fresh snapshot using eXist-db's `bin/backup.sh` over XML-RPC to the running instance. Retention is the responsibility of the surrounding backup tool (Borg, Restic, ...) which snapshots that directory.

### Optional Backup Variables

`existdb__dump_collection`

* Collection to back up. `/db` is the eXist-db root and covers everything.
* Type: String.
* Default: `'/db'`

`existdb__dump_directory`

* Where the latest snapshot lands. Owned by `{{ existdb__user }}:{{ existdb__group }}`.
* Type: String.
* Default: `'/backup/existdb-dump'`

`existdb__dump_enabled`

* Enables or disables the timer.
* Type: Bool.
* Default: `true`

`existdb__dump_on_calendar`

* `OnCalendar=` value for `existdb-dump.timer`. Default seeds the minute by `inventory_hostname` so a fleet does not all hit eXist-db at the same second.
* Type: String.
* Default: `'*-*-* 22:{{ 59 | random(seed=inventory_hostname) }}:00'`

`existdb__dump_password`

* Password the dumper uses to connect. Defaults to `existdb__admin_password`.
* Type: String.
* Default: `'{{ existdb__admin_password }}'`

`existdb__dump_user`

* User the dumper authenticates as. eXist-db has no separate "backup" role, so this typically stays `admin`.
* Type: String.
* Default: `'admin'`

### Restoring a Backup

1. The dumper writes a flat tree under `existdb__dump_directory` rooted at the backed-up collection name. With the default `existdb__dump_collection: '/db'` the layout is:

    ```
    /backup/existdb-dump/db/__contents__.xml
    /backup/existdb-dump/db/<sub-collection>/__contents__.xml
    ...
    ```

2. With eXist-db running, replay the backup via `bin/restore.sh`:

    ```bash
    runuser -u existdb -- /opt/existdb/bin/restore.sh \
        -u admin \
        -p '<admin password>' \
        -r /backup/existdb-dump/db/__contents__.xml \
        -ouri=xmldb:exist://127.0.0.1:8888/exist/xmlrpc
    ```

    The path passed to `-r` must be the `__contents__.xml` at the root of the backup tree. The `-ouri=...` (no space, as in the eXist-db docs) is required because `bin/restore.sh` ignores `$EXIST_HOME/etc/client.properties` at runtime and falls back to the compiled-in default `xmldb:exist://localhost:8080/exist/xmlrpc`. On dual-stack hosts `localhost` resolves to `::1` first but eXist-db's Jetty binds IPv4 only, surfacing as `HTTP server returned unexpected status: null`. `runuser` is preferred over `sudo` for the same reason as in the dump script — `sudo`'s PAM session swallows the Java stderr without a TTY.

3. The restore overwrites collections in place. Verify via the eXist-db admin UI at `http://<host>:{{ existdb__http_port }}/exist/`.

For full disaster recovery (host loss): re-run the role first to reinstall eXist-db at the same version with the same admin password, then run `restore.sh`.


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
