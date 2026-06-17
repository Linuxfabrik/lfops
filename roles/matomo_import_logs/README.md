# Ansible Role linuxfabrik.lfops.matomo_import_logs

This role imports Apache (or other) access logs into [Matomo](https://matomo.org/) on a schedule. For each configured site it deploys a systemd timer that runs the Matomo log-analytics import script ([import_logs.py](https://github.com/matomo-org/matomo-log-analytics)) against the access log of the day. The role also ships the import script itself to `/usr/local/sbin/import_logs.py`.

This is the batch counterpart to the realtime piped-log tracking documented in the [linuxfabrik.lfops.apache_httpd](https://github.com/Linuxfabrik/lfops/tree/main/roles/apache_httpd) role. Both share the same `import_logs.py`, which this role deploys.


*Available in the next LFOps release.*


## How the Role Behaves

* The import script is deployed on every run to `/usr/local/sbin/import_logs.py`, even when no sites are configured. Hosts that use the realtime piped-log tracking of the `apache_httpd` role therefore need this role too.
* For every site in `matomo_import_logs__sites` the role deploys a per-site auth file under `/etc/matomo-import-logs/`, a oneshot `*.service`, and a `*.timer`. The auth file is mode `0600` and holds the `token_auth`, so the token never appears in the process list (passing it via `--token-auth` on the command line is deprecated and logs a warning).
* The dated access-log file is resolved at runtime by the service, so the timer always imports the log of the day it fires. `log_file` is passed through `date`, so it may contain `strftime` tokens such as `%Y%m%d`.
* Sites set to `state: 'absent'` have their timer, service, and auth file removed.
* This role does not create the Matomo site or the `token_auth`. Provision those in Matomo first.


## Dependent Roles

Any [LFOps playbook](https://github.com/Linuxfabrik/lfops/blob/main/playbooks/README.md) that installs this role runs these for you. Optional ones can be disabled via the playbook's skip variables.

* Python 3 must be present, as the import script runs under `/usr/bin/env python3` (role: [linuxfabrik.lfops.python](https://github.com/Linuxfabrik/lfops/tree/main/roles/python)).


## Requirements

Manual steps:

* Create the target site in Matomo and obtain a `token_auth` with at least `admin` (or super user) permission. Store it in your inventory, ideally via the [linuxfabrik.lfops.bitwarden_item](https://github.com/Linuxfabrik/lfops/tree/main/roles/bitwarden_item) lookup.


## Tags

`matomo_import_logs`

* Deploys the import script, the per-site auth files, and the systemd units.
* Manages the per-site timers (enable / start, or disable / stop).
* Triggers: systemctl daemon-reload.

`matomo_import_logs:configure`

* Deploys the per-site auth files and systemd units, and removes the artifacts of absent sites.
* Triggers: systemctl daemon-reload.

`matomo_import_logs:state`

* Manages the runtime state of the per-site timers (enable / start / disable / stop).
* Triggers: none.


## Optional Role Variables

`matomo_import_logs__sites__host_var` / `matomo_import_logs__sites__group_var`

* The sites whose access logs are imported into Matomo. Items are identified by `name`.
* Type: List of dictionaries.
* Default: `[]`
* Subkeys:

    * `name`:

        * Mandatory. Site identifier, used for the unit, timer, and auth file names. Use the FQDN.
        * Type: String.

    * `idsite`:

        * Mandatory. The Matomo site ID to import into.
        * Type: Number.

    * `url`:

        * Mandatory. The Matomo base URL.
        * Type: String.

    * `token_auth`:

        * Mandatory. The Matomo `token_auth`. Written to the auth file, never passed on the command line.
        * Type: String.

    * `log_file`:

        * Mandatory. Path of the access log to import. Passed through `date`, so it may contain `strftime` tokens (e.g. `%Y%m%d`) that resolve at runtime.
        * Type: String.

    * `log_file_date`:

        * Optional. The `date --date=` reference used to resolve `log_file`.
        * Type: String.
        * Default: `'today'`

    * `log_format_name`:

        * Optional. The import script's log format. The `matomo` LogFormat of the `apache_httpd` role matches `common_complete`.
        * Type: String.
        * Default: `'common_complete'`

    * `recorders`:

        * Optional. Number of parallel import threads.
        * Type: Number.
        * Default: `1`

    * `options`:

        * Optional. Extra command-line options passed to the import script (e.g. `--enable-reverse-dns`, `--enable-http-errors`).
        * Type: List of strings.
        * Default: `[]`

    * `output`:

        * Optional. File the import script writes its own output to.
        * Type: String.
        * Default: `'/var/log/matomo.log'`

    * `on_calendar`:

        * Optional. The timer schedule, in systemd `OnCalendar` syntax.
        * Type: String.
        * Default: `'06:30'`

    * `enabled`:

        * Optional. Whether the timer is enabled and started.
        * Type: Bool.
        * Default: `true`

    * `state`:

        * Optional. `present` or `absent`. `absent` removes the timer, service, and auth file.
        * Type: String.
        * Default: `'present'`

Example:
```yaml
# optional
matomo_import_logs__sites__host_var:
  - name: 'www.example.com'
    idsite: 1
    url: 'https://matomo.example.com'
    token_auth: 'linuxfabrik'
    log_file: '/var/log/httpd/www.example.com-access.log-%Y%m%d'
    recorders: 2
    options:
      - '--enable-reverse-dns'
    on_calendar: '06:30'
  - name: 'old-site.example.com'
    state: 'absent'
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
