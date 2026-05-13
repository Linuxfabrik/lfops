# Ansible Role linuxfabrik.lfops.fangfrisch

This role installs and configures [Fangfrisch](https://rseichter.github.io/fangfrisch/), a tool that "allows downloading virus definition files that are not official ClamAV canon".


*Available since LFOps `3.0.0`.*

* A Python virtual environment `/opt/python-venv/clamav-fangfrisch/` with `fangfrisch` installed. This can be done using the [linuxfabrik.lfops.python_venv](https://github.com/linuxfabrik/lfops/tree/main/roles/python_venv) role.
* On Rocky 9+, the EPEL and the CRB Repo ("Code Ready Builder") need to be enabled to be able to install `python3-virtualenv`. This can be done using the [linuxfabrik.lfops.repo_epel](https://github.com/linuxfabrik/lfops/tree/main/roles/repo_epel) and [linuxfabrik.lfops.repo_baseos](https://github.com/linuxfabrik/lfops/tree/main/roles/repo_baseos) roles.

## Dependent Roles

Any [LFOps playbook](https://github.com/Linuxfabrik/lfops/blob/main/playbooks/README.md) that installs this role runs these for you. Optional ones can be disabled via the playbook's skip variables.

* A Python virtual environment `/opt/python-venv/clamav-fangfrisch/` with `fangfrisch` installed must be present (role: [linuxfabrik.lfops.python_venv](https://github.com/linuxfabrik/lfops/tree/main/roles/python_venv)).


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

`fangfrisch__timer_enabled`

* Enables or disables the hourly fangfrisch timer to automatically update the signatures, analogous to `systemctl enable/disable`.
* Type: Bool.
* Default: `true`

Example:
```yaml
# optional
fangfrisch__securiteinfo_customer_id: 'IVQyhw7Yszua6pzUhlGPVowucenHt2wQe9iXDfwsMOfheeOUakB28irj5JyDsKF4e81LkLbNUtMHcUGL9EVKOJ9WxSSv4ySjBhY0vngBDunEPlixtGTBB6f1mvaTqXzz'
fangfrisch__timer_enabled: false
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
