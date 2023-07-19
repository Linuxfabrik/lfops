# Ansible Role linuxfabrik.lfops.fangfrisch

This role installs and configures [Fangfrisch](https://rseichter.github.io/fangfrisch/), a tool that "allows downloading virus definition files that are not official ClamAV canon".

Runs on

* RHEL 8 (and compatible)


## Mandatory Requirements

* A Python virtual environment `/opt/python-venv/clamav-fangfrisch/` with `fangfrisch` installed. This can be done using the [linuxfabrik.lfops.python_venv](https://github.com/linuxfabrik/lfops/tree/main/roles/python_venv) role.

If you use the [Fangfrisch Playbook](https://github.com/Linuxfabrik/lfops/blob/main/playbooks/fangfrisch.yml), this is automatically done for you.


## Tags

| Tag                | What it does                              |
| ---                | ------------                              |
| `fangfrisch`       | Installs and configures Fangfrisch        |
| `fangfrisch:state` | Manages the state of the Fangfrisch timer |


## Optional Role Variables

| Variable | Description | Default Value |
| -------- | ----------- | ------------- |
| `fangfrisch__malwarepatrol_receipt` | Set this to enable downloading signatures from [MalwarePatrol](https://www.malwarepatrol.net). Requires an [MalwarePatrol account](https://www.malwarepatrol.net/my-account/). | unset |
| `fangfrisch__securiteinfo_customer_id` | Set this to enable downloading signatures from [SecuriteInfo](https://www.securiteinfo.com/). Requires an [SecuriteInfo account](https://www.securiteinfo.com/clients/customers/account). | unset |
| `fangfrisch_timer_enabled` | Enables or disables the hourly fangfrisch timer to automatically update the signatures, analogous to `systemctl enable/disable`. | `true` |

Example:
```yaml
# optional
fangfrisch__malwarepatrol_receipt: 'wtNJNBPsNJN'
fangfrisch__securiteinfo_customer_id: 'IVQyhw7Yszua6pzUhlGPVowucenHt2wQe9iXDfwsMOfheeOUakB28irj5JyDsKF4e81LkLbNUtMHcUGL9EVKOJ9WxSSv4ySjBhY0vngBDunEPlixtGTBB6f1mvaTqXzz'
fangfrisch_timer_enabled: false
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
