# Ansible Role linuxfabrik.lfops.fail2ban

This role installs and configures [fail2ban](https://www.fail2ban.org).

This role provides two additional filters:

* apache-dos: Matches all incoming requests to Apache. Can be used to limit the number of allowed requests per client.
* portscan: Instantly blocks an IP if it accesses a non-permitted port. Note that this requires an iptables firewall with logging (for example, fwbuilder).


## Mandatory Requirements

* Install the `python3-policycoreutils` module (required for the SELinux Ansible tasks). This can be done using the [linuxfabrik.lfops.policycoreutils](https://github.com/Linuxfabrik/lfops/tree/main/roles/policycoreutils) role.
* On RHEL-compatible systems, enable the EPEL repository. This can be done using the [linuxfabrik.lfops.repo_epel](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_epel) role.
* On RHEL-compatible systems, enable the `nis_enabled` SELinux boolean. This can be done using the [linuxfabrik.lfops.selinux](https://github.com/Linuxfabrik/lfops/tree/main/roles/selinux) role.

If you use the ["Fail2Ban" Playbook](https://github.com/Linuxfabrik/lfops/blob/main/playbooks/fail2ban.yml), this is automatically done for you.

## Tags

| Tag              | What it does                              | Reload / Restart |
| ---              | ------------                              | ---------------- |
| `fail2ban`       | Installs and configures fail2ban          | Restarts fail2ban.service |
| `fail2ban:state` | Manages the state of the fail2ban service | - |


## Optional Role Variables

| Variable | Description | Default Value |
| -------- | ----------- | ------------- |
| `fail2ban__jail_default_action` | The default action. This will be used in all jails which do not overwrite it. | `fail2ban__jail_default_banaction` |
| `fail2ban__jail_default_banaction` | The default banaction, which will be executed as defined in `fail2ban__jail_default_action` (assuming the jail does not overwrite it). | `'iptables-multiport'` |
| `fail2ban__jail_default_ignoreip` | List of IP addresses (in CIDR notation) that will be ignored from all jails (assuming the jail does not overwrite it). | `[]` |
| `fail2ban__jail_default_rocketchat_hook` | The incoming Rocket.Chat hook which will be used to send a notification on bans. For this to work `rocketchat` has to be in the action, have a look at `fail2ban__jail_default_action` (example below). | `''` |
| `fail2ban__jail_portscan_allowed_ports` | A list of ports which are allowed to be accessed. IPs accessing these ports will not be blocked. Note: This setting is for the portscan jail. | `[22]` |
| `fail2ban__jail_portscan_server_ips` | A list of IP addresses of the server. Only traffic destined for these IPs will be considered. This prevents accidental banning due to traffic which is passing by the server, but not destined for it. Note: This setting is for the portscan jail. | `'{{ ansible_facts["all_ipv4_addresses"] }}'` |
| `fail2ban__jails__group_var` / `fail2ban__jails__host_var` | The fail2ban jail definition. Subkeys: <ul><li>`template`: Mandatory, string. Name of the Jinja template source file to use. Have a look at the possible options [here](https://github.com/Linuxfabrik/lfops/tree/main/roles/fail2ban/templates/etc/fail2ban/jail.d), or `raw`.</li> <li>`filename`: Mandatory, string. Destination filename in `jail.d/`, and normally is equal to the name of the source `template` used. Will be suffixed with `.conf`.</li> <li>`state`: Mandatory, string. State of the jail. Possible options: `absent`, `present`.</li> <li>`raw`: Optional, string: Raw content for the jail.</li></ul> <br>For the usage in `host_vars` / `group_vars` (can only be used in one group at a time). | <ul><li>`z10-portscan`</li><li>`z10-sshd`</li></ul> |
| `fail2ban__service_enabled` | Enables or disables the fail2ban service, analogous to `systemctl enable/disable --now`. Possible options: | `true` |

Example:
```yaml
# optional
fail2ban__jail_default_action: |-
  %(banaction)s[name=%(__name__)s, bantime="%(bantime)s", port="%(port)s", protocol="%(protocol)s", chain="%(chain)s"]
  rocketchat[name=%(__name__)s, rocketchat-hook="%(rocketchat-hook)s"]
fail2ban__jail_default_banaction: 'iptables-multiport'
fail2ban__jail_default_ignoreip:
  - '192.0.2.1/32' # ansible deployment host
fail2ban__jail_default_rocketchat_hook: ''
fail2ban__jail_portscan_allowed_ports:
  - 22
fail2ban__jail_portscan_server_ips:
  - '192.0.2.5'
  - '198.51.100.100'
fail2ban__jails__host_var:
  - filename: 'z10-apache-dos'
    state: 'absent'
    template: 'apache-dos'
  - filename: 'z20-custom-apache-dos'
    state: 'present'
    template: 'raw'
    raw: |-
      [apache-dos]
      bantime  = 5m
      enabled  = true
      findtime = 10s
      logpath  = /var/log/httpd/*access?log
      maxretry = 600
      port     = http,https
fail2ban__service_enabled: true
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
