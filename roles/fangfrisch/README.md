# Ansible Role linuxfabrik.lfops.fangfrisch

This role installs and configures [Fangfrisch](https://rseichter.github.io/fangfrisch/), a tool that "allows downloading virus definition files that are not official ClamAV canon".


*Available since LFOps `3.0.0`.*


## Dependent Roles

Any [LFOps playbook](https://github.com/Linuxfabrik/lfops/blob/main/playbooks/README.md) that installs this role runs these for you. Optional ones can be disabled via the playbook's skip variables.

* A Python virtual environment `/opt/python-venv/clamav-fangfrisch/` with `fangfrisch` installed must be present (role: [linuxfabrik.lfops.python_venv](https://github.com/linuxfabrik/lfops/tree/main/roles/python_venv)).
* On Rocky 9+, the EPEL repository (role: [linuxfabrik.lfops.repo_epel](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_epel)) and the CRB ("Code Ready Builder") repository (role: [linuxfabrik.lfops.repo_baseos](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_baseos)) must be enabled so `python3-virtualenv` can be installed.


## How the Role Behaves

* Fangfrisch always downloads the [Sanesecurity](https://sanesecurity.com/) signatures. The SecuriteInfo and URLhaus signatures need an account with the provider and are only downloaded once `fangfrisch__securiteinfo_customer_id` or `fangfrisch__urlhaus_auth_key` is set.
* On its next refresh, Fangfrisch removes the signatures it downloaded from a source that is no longer enabled.


## Tags

`fangfrisch`

* Installs and configures Fangfrisch.
* Triggers: none.

`fangfrisch:state`

* Manages the state of the Fangfrisch timer.
* Triggers: none.


## Optional Role Variables

`fangfrisch__securiteinfo_customer_id`

* Set this to enable downloading signatures from [SecuriteInfo](https://www.securiteinfo.com/). Requires a [SecuriteInfo account](https://www.securiteinfo.com/clients/customers/account).
* Type: String.
* Default: unset

`fangfrisch__urlhaus_auth_key`

* Set this to enable downloading signatures from [URLhaus](https://urlhaus.abuse.ch/). Requires an Auth-Key from the [abuse.ch Authentication Portal](https://auth.abuse.ch/).
* Type: String.
* Default: unset

`fangfrisch__timer_enabled`

* Enables or disables the hourly fangfrisch timer to automatically update the signatures, analogous to `systemctl enable/disable`.
* Type: Bool.
* Default: `true`

Example:
```yaml
# optional
fangfrisch__securiteinfo_customer_id: 'linuxfabrik'
fangfrisch__timer_enabled: false
fangfrisch__urlhaus_auth_key: 'linuxfabrik'
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
