# Ansible Role linuxfabrik.lfops.snmp

This role installs and configures snmp.


## Tags

| Tag           | What it does                               |
| ---           | ------------                               |
| `snmp`        | Installs and configures snmp               |
| `snmp:state`  | Starts, stops or restarts the snmp daemon  |


## Optional Role Variables

| Variable | Description | Default Value |
| -------- | ----------- | ------------- |
| `snmp__rocommunity` | Sets the SNMPv1 + SNMPv2 readonly community. | `'mypublic'` |
| `snmp__syscontact` | Sets the systemcontact information. | `'Root <root@localhost>'` |
| `snmp__syslocation` | Sets the location of the system. | `'unknown'` |


Example:
```yaml
# optional
snmp__rocommunity: 'myreadonlycommunity'
snmp__syscontact: 'webmaster@example.com'
snmp__syslocation: 'Datacenter Zurich'
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
