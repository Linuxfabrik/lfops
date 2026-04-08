# Ansible Role linuxfabrik.lfops.snmp

This role installs and configures snmp.


## Tags

`snmp`

* Installs and configures snmp.
* Triggers: snmpd.service restart.

`snmp:state`

* Starts, stops or restarts the snmp daemon.
* Triggers: none.


## Optional Role Variables

`snmp__rocommunity`

* Sets the SNMPv1 + SNMPv2 readonly community.
* Type: String.
* Default: `'mypublic'`

`snmp__snmpd_service_enabled`

* Enables or disables the snmpd service, analogous to `systemctl enable/disable --now`.
* Type: Bool.
* Default: `true`

`snmp__syscontact`

* Sets the systemcontact information.
* Type: String.
* Default: `'Root <root@localhost>'`

`snmp__syslocation`

* Sets the location of the system.
* Type: String.
* Default: `'unknown'`


Example:
```yaml
# optional
snmp__rocommunity: 'myreadonlycommunity'
snmp__snmpd_service_enabled: true
snmp__syscontact: 'webmaster@example.com'
snmp__syslocation: 'Datacenter Zurich'
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
