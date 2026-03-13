# Ansible Role linuxfabrik.lfops.crypto_policy

This role sets the crypto policy for the system. In addition, it implements and deploys crypto policies defined by Linuxfabrik, e.g. to support CIS hardening.


## Tags

| Tag             | What it does                  | Reload / Restart |
| ---             | ------------                  | ---------------- |
| `crypto_policy` | Sets the system crypto policy | - |


## Optional Role Variables

| Variable | Description | Default Value |
| -------- | ----------- | ------------- |
| `crypto_policy__policy` | String. The crypto policy to activate. See `roles/crypto_policy/templates/etc/crypto-policies/policies/modules/` for a list of available crypto policies. Example: `DEFAULT:LINUXFABRIK-NO-SHA1:LINUXFABRIK-SSH-NO-CBC` | <ul><li>RedHat8:<br>`'DEFAULT:LINUXFABRIK-NO-SHA1:LINUXFABRIK-NO-WEAKMAC:LINUXFABRIK-SSH-NO-CBC:LINUXFABRIK-SSH-NO-CHACHA20'`</li><li>RedHat9:<br>`'DEFAULT:LINUXFABRIK-NO-SHA1:LINUXFABRIK-NO-WEAKMAC:LINUXFABRIK-SSH-NO-CBC:LINUXFABRIK-SSH-NO-CHACHA20:LINUXFABRIK-SSH-NO-ETM'`</li><li>RedHat10:<br>`'DEFAULT:LINUXFABRIK-NO-SHA1:LINUXFABRIK-NO-WEAKMAC:LINUXFABRIK-SSH-NO-CBC:LINUXFABRIK-SSH-NO-CHACHA20:LINUXFABRIK-SSH-NO-ETM'`</li></ul> |

Example:
```yaml
# optional
crypto_policy__policy: 'DEFAULT:LINUXFABRIK-NO-SHA1:LINUXFABRIK-NO-WEAKMAC:LINUXFABRIK-SSH-NO-CBC:LINUXFABRIK-SSH-NO-CHACHA20:LINUXFABRIK-SSH-NO-ETM'
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
