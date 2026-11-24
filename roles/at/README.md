# Ansible Role linuxfabrik.lfops.at

This role installs at, a daemon that allows commands to be run at a specified time.


*Available since LFOps `2.0.0`.*


## How the Role Behaves

* Only root and the users in `at__allow_users__*_var` may submit, list or remove at jobs, as the CIS Benchmarks require. The role writes them to `/etc/at.allow`, which makes `at` ignore `/etc/at.deny`. Jobs queued before still run.
* On the Red Hat family, `/etc/at.allow` and `/etc/at.deny` get mode `0600`, owned by `root:root`. On Debian and Ubuntu, `at` reads them as group `daemon`, so `/etc/at.allow` gets `root:daemon` `0640` and `/etc/at.deny` keeps the `root:daemon` `0640` the package ships. Do not change this to `root:root`: if `at` cannot read `/etc/at.allow`, it falls back to `/etc/at.deny` and lets every user not listed there use `at`.
* `/etc/at.allow` is overwritten on every run, a timestamped backup is kept.


## Tags

`at`

* Installs and configures at/atd.
* Deploys `/etc/at.allow`.
* Restricts the mode of `/etc/at.deny`.
* Triggers: none.

`at:state`

* Manages the state of `atd.service` (enable/disable at boot, plus start/stop/restart/reload).
* Triggers: none.


## Optional Role Variables

`at__allow_users__host_var` / `at__allow_users__group_var`

* Users besides root that may use `at`, `atq` and `atrm`.
* Type: List of dictionaries.
* Default: `[]`
* Deviates from the upstream default, which ships no `/etc/at.allow` and so lets every user not listed in `/etc/at.deny` schedule jobs: an allow list cannot miss an account added later.
* Subkeys:

    * `name`:

        * Mandatory. User name.
        * Type: String.

    * `state`:

        * Optional. `present` or `absent`.
        * Type: String.
        * Default: `'present'`

`at__service_enabled`

* Whether `atd.service` is enabled at boot, analogous to `systemctl enable / disable`.
* Type: Bool.
* Default: `true`

`at__service_state`

* State of `atd.service`, analogous to `systemctl start / stop / restart / reload`.
* Type: String. One of `reloaded`, `restarted`, `started`, `stopped`.
* Default: `'started'` if `at__service_enabled` is `true`, otherwise `'stopped'`.

Example:
```yaml
# optional
at__allow_users__host_var:
  - name: 'backup'
  - name: 'olduser'
    state: 'absent'
at__service_enabled: true
at__service_state: 'started'
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
