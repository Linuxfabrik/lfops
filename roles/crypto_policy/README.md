# Ansible Role linuxfabrik.lfops.crypto_policy

This role sets the crypto policy for the system. In addition, it implements and deploys crypto policies defined by Linuxfabrik, e.g. to support CIS hardening.


## Tags

`crypto_policy`

* Sets the system crypto policy.
* Triggers: none.


## Optional Role Variables

`crypto_policy__policy`

* The crypto policy to activate. See `roles/crypto_policy/templates/etc/crypto-policies/policies/modules/` for a list of available crypto policies. Example: `DEFAULT:LINUXFABRIK-NO-SHA1:LINUXFABRIK-SSH-NO-CBC`
* Type: String.
* Default:
    * RedHat8: `'DEFAULT:LINUXFABRIK-NO-SHA1:LINUXFABRIK-NO-WEAKMAC:LINUXFABRIK-SSH-NO-CBC:LINUXFABRIK-SSH-NO-CHACHA20'`
    * RedHat9: `'DEFAULT:LINUXFABRIK-NO-SHA1:LINUXFABRIK-NO-WEAKMAC:LINUXFABRIK-SSH-NO-CBC:LINUXFABRIK-SSH-NO-CHACHA20:LINUXFABRIK-SSH-NO-ETM'`
    * RedHat10: `'DEFAULT:LINUXFABRIK-NO-SHA1:LINUXFABRIK-NO-WEAKMAC:LINUXFABRIK-SSH-NO-CBC:LINUXFABRIK-SSH-NO-CHACHA20:LINUXFABRIK-SSH-NO-ETM'`

Example:
```yaml
# optional
crypto_policy__policy: 'DEFAULT:LINUXFABRIK-NO-SHA1:LINUXFABRIK-NO-WEAKMAC:LINUXFABRIK-SSH-NO-CBC:LINUXFABRIK-SSH-NO-CHACHA20:LINUXFABRIK-SSH-NO-ETM'
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
