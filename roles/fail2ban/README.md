# Ansible Role fail2ban

This role installs and configures [fail2ban](https://www.fail2ban.org).

This role provides two additional filters:

* apache-dos: Matches all incoming requests to Apache. Can be used to limit the number of allowed requests per client.
* portscan: Instantly blocks an IP if it accesses a non-permitted port. Note that this requires an iptables firewall with logging (for example, fwbuilder).

FQCN: linuxfabrik.lfops.fail2ban

Tested on

* RHEL 8 (and compatible)


## Requirements

### Mandatory

* Install the `python3-policycoreutils` module (required for the SELinux Ansible tasks).
* On RHEL-compatible systems, enable the EPEL repository. This can be done using the [linuxfabrik.lfops.repo_epel](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_epel) role.


### Optional

This role does not have any optional requirements.


## Tags

| Tag            | What it does                              |
| ---            | ------------                              |
| fail2ban       | Installs and configures fail2ban          |
| fail2ban:state | Manages the state of the fail2ban service |


## Role Variables

Have a look at the [defaults/main.yml](https://github.com/Linuxfabrik/lfops/blob/main/roles/fail2ban/defaults/main.yml) for the variable defaults.


### Mandatory

This role does not have any mandatory variables.


### Optional

#### fail2ban__jail_default_action

The default action. This will be used in all jails which do not overwrite it. Defaults to `fail2ban__jail_default_banaction` and notifying via Rocket.Chat.

Default:
```yaml
fail2ban__jail_default_action: |-
  %(banaction)s[name=%(__name__)s, bantime="%(bantime)s", port="%(port)s", protocol="%(protocol)s", chain="%(chain)s"]
  rocketchat[name=%(__name__)s, rocketchat-hook="%(rocketchat-hook)s"]
```


#### fail2ban__jail_default_banaction

The default banaction, which will be executed as defined in `fail2ban__jail_default_action` (assuming the jail does not overwrite it).

Default:
```yaml
fail2ban__jail_default_banaction: 'iptables-multiport'
```


#### fail2ban__jail_default_ignoreip

List of IP addresses (in CIDR notation) that will be ignored from all jails (assuming the jail does not overwrite it).

Default:
```yaml
fail2ban__jail_default_ignoreip: []
```

Example:
```yaml
fail2ban__jail_default_ignoreip:
  - '192.0.2.1/32' # ansible deployment host
```


#### fail2ban__jail_default_rocketchat_hook

The incoming Rocket.Chat hook which will be used to send a notification on bans. For this to work `rocketchat` has to be in the action, have a look at `fail2ban__jail_default_action`.

Default:
```yaml
fail2ban__jail_default_rocketchat_hook: ''
```


#### fail2ban__service_enabled

Enables or disables the fail2ban service, analogous to `systemctl enable/disable --now`. Possible options:

* true
* false

Default:
```yaml
fail2ban__service_enabled: true
```


#### fail2ban__jail_portscan_allowed_ports

A list of ports which are allowed to be accessed. IPs accessing these ports will not be blocked.

Note: This setting is for the portscan jail.

Default:
```yaml
fail2ban__jail_portscan_allowed_ports:
  - 22
```


#### fail2ban__jail_portscan_server_ips

A list of IP addresses of the server. Only traffic destined for these IPs will be considered. This prevents accidental banning due to traffic which is passing by the server, but not destined for it.

Note: This setting is for the portscan jail.

Default:
```yaml
fail2ban__jail_portscan_server_ips: '{{ ansible_facts["all_ipv4_addresses"] }}'
```

Example:
```yaml
fail2ban__jail_portscan_server_ips:
  - '192.0.2.5'
  - '198.51.100.100'
```


#### fail2ban__host_jails / fail2ban__group_jails

These variables are intended to be used in a host / group variable file in the Ansible inventory. Note that the group variable can only be used in one group at a time.

A list of dictionaries containing definitions for the virtual environments.

Subkeys:

* `name`: Required, string. The name of the jail. Can either be one of the pre-defined ones (`type: conf`), or a custom one (`type: raw`):
    * apache-badbots
    * apache-botsearch
    * apache-dos
    * apache-fakegooglebot
    * apache-nohome
    * apache-noscript
    * apache-overflows
    * portscan
    * sshd
* `state`: Required, boolean. State of the jail. Possible options: `absent`, `present`.
* `type`: Optional, boolean. Type of the jail. Either `conf` to use one of the pre-defined ones, or `raw` to deploy a custom jail. Defaults to `conf`.
* `raw`: Optional, string: Raw content for the custom jail.

Default:
```yaml
fail2ban__group_jails: []
fail2ban__host_jails: []
fail2ban__role_jails:
  - name: 'portscan'
    state: 'present'
    type: 'conf'

  - name: 'sshd'
    state: 'present'
    type: 'conf'
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
