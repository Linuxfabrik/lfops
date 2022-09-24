# Ansible Role linuxfabrik.lfops.crypto_policy

This role sets the system crypto policy. Additionally, it deploys crypto policies modified by Linuxfabrik to allow things such as the EPEL-release and ssh-ed25519 keys.

Runs on

* RHEL 8 (and compatible)


## Tags

| Tag             | What it does                  |
| ---             | ------------                  |
| `crypto_policy` | Sets the system crypto policy |


## Optional Role Variables

| Variable | Description | Default Value |
| -------- | ----------- | ------------- |
| `crypto_policy__policy` | The crypto policy to activate. Possible options:<br> * `FIPS:LINUXFABRIK-FIPS`<br> * `FUTURE:LINUXFABRIK-FUTURE`<br> * any listed in `man 7 crypto-policies` | `'FUTURE:LINUXFABRIK-FUTURE'` |

Example:
```yaml
# optional
crypto_policy__policy: 'FUTURE:LINUXFABRIK-FUTURE'
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
