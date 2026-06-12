# Ansible Role linuxfabrik.lfops.crypto_policy

On Red Hat-family systems, `update-crypto-policies` is a system-wide switch that picks the allowed TLS / SSH / IPsec / Kerberos algorithm sets for *all* crypto-aware services in one place (e.g. `DEFAULT`, `LEGACY`, `FUTURE`, `FIPS`). This role sets that policy and additionally ships custom sub-policies defined by Linuxfabrik, e.g. to support CIS hardening.


*Available since LFOps `2.0.0`.*


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
