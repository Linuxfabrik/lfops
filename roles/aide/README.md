# Ansible Role linuxfabrik.lfops.aide

This role ensures that AIDE is installed, configured, and scheduled for regular filesystem integrity checks.

* The initial AIDE database is created only if `/var/lib/aide/aide.db.gz` does not already exist.
* Many default paths are pre-configured in the AIDE config for exclusion and inclusion rules.
* Exclusion always takes precedence over inclusion for any given path.


## Tags

| Tag | What it does | Reload / Restart |
| --- | ------------ | ---------------- |
| `aide` | Runs all tasks of the role | - |
| `aide:configure` | Deploys `/etc/aide.conf` | - |
| `aide:install` | Installs the AIDE package and initializes the AIDE database if it does not exist yet | - |
| `aide:state` | Deploys the `aide-check.service` and `aide-check.timer` systemd units and sets the desired state | Reloads systemd daemon if unit files changed |
| `aide:update_db` | Rebuilds the AIDE database; only runs if called explicitly | - |


## Optional Role Variables

`aide__check_time_on_calendar`

* The time at which the AIDE check runs. See [systemd.time(7)](https://www.freedesktop.org/software/systemd/man/systemd.time.html) for the format.
* Type: String.
* Default: `'*-*-* 05:00:00'`

`aide__exclude_recursive__host_var` / `aide__exclude_recursive__group_var`

* Paths to exclude recursively from AIDE monitoring (prepended with `!` in the config).
* Type: List of dictionaries.
* Default: `[]`
* Subkeys:

    * `path`:

        * Mandatory. Filesystem path to exclude recursively.
        * Type: String.

    * `state`:

        * Optional. `present` or `absent`.
        * Type: String.
        * Default: `'present'`

`aide__exclude_rules__host_var` / `aide__exclude_rules__group_var`

* Paths to exclude from AIDE monitoring (prepended with `-` in the config).
* Type: List of dictionaries.
* Default: `[]`
* Subkeys:

    * `path`:

        * Mandatory. Filesystem path to exclude.
        * Type: String.

    * `state`:

        * Optional. `present` or `absent`.
        * Type: String.
        * Default: `'present'`

`aide__include_rules__host_var` / `aide__include_rules__group_var`

* Additional paths to monitor with a specific rule set.
* Type: List of dictionaries.
* Default:

    ```yaml
    - path: '/opt/python-venv'
      attributes: 'CONTENT'
    ```

* Subkeys:

    * `path`:

        * Mandatory. Filesystem path to monitor.
        * Type: String.

    * `attributes`:

        * Mandatory. AIDE rule set to apply (e.g. `CONTENT`, `CONTENT_EX`, `PERMS`, `NORMAL`).
        * Type: String.

    * `state`:

        * Optional. `present` or `absent`.
        * Type: String.
        * Default: `'present'`

`aide__timer_enabled`

* Enables or disables the `aide-check.timer`, analogous to `systemctl enable/disable`.
* Type: Bool.
* Default: `true`

`aide__timer_state`

* Sets the state of the `aide-check.timer`, analogous to `systemctl start/stop`.
* Type: String. One of `started`, `stopped`.
* Default: `'started'`

Example:
//TODO: use test cases here, after test has been done

## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
