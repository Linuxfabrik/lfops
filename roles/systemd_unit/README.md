# Ansible Role linuxfabrik.lfops.systemd_unit

This role installs and manages systemd unit files. A unit file is a plain text ini-style file that encodes information about a service, a socket, a device, a mount point, an automount point, a swap file or partition, a start-up target, a watched file system path, a timer controlled and supervised by systemd, a resource management slice or a group of externally created processes. See `systemd.unit` for unit configuration, `systemd.syntax(7)` for a general description of the syntax, and [load-fragment-gperf.gperf.in](https://github.com/systemd/systemd/blob/main/src/core/load-fragment-gperf.gperf.in) for a list of all directives and their context.


## Tags

`systemd_unit`

* Remove service units from `/etc/systemd/system`.
* Deploy the service units to `/etc/systemd/system`.
* Remove timer units from `/etc/systemd/system`.
* Deploy the timer units to `/etc/systemd/system`.
* Triggers: systemctl daemon-reload.

`systemd_unit:mounts`

* Manages systemd mount units.
* Triggers: systemctl daemon-reload.

`systemd_unit:services`

* Remove service units from `/etc/systemd/system`.
* Deploy the service units to `/etc/systemd/system`.
* Triggers: systemctl daemon-reload.

`systemd_unit:state`

* Manages the state of the unit file.
* Triggers: none.

`systemd_unit:timers`

* Remove timer units from `/etc/systemd/system`.
* Deploy the timer units to `/etc/systemd/system`.
* Triggers: systemctl daemon-reload.


## Optional Role Variables

`systemd_unit__mounts__host_var` / `systemd_unit__mounts__group_var`

* List of Systemd Mount Units.
* Type: List of dictionaries.
* Default: `[]`
* Subkeys:

    * `name`:

        * Mandatory. Name of the systemd mount. Will be used as the filename. Note mount units must be named after the mount point directories they control. Use `systemd-escape --path /mnt/my-folder`.
        * Type: String.

    * `description`:

        * Optional. The description for the unit. If ommitted, the name will be used, suffixed by `Mount`.
        * Type: String.
        * Default: unset

    * `wanted_by`:

        * Optional. Value for `WantedBy`.
        * Type: String.
        * Default: `'default.target'`

    * `raw_unit`:

        * Optional. Raw block in the `[Unit]` section.
        * Type: String.
        * Default: unset

    * `raw_mount`:

        * Optional. Raw block in the `[Mount]` section.
        * Type: String.
        * Default: unset

    * `raw_install`:

        * Optional. Raw block in the `[Install]` section.
        * Type: String.
        * Default: unset

    * `state`:

        * Optional. State of the unit. Possible options: `present`, `absent`, `started`, `stopped`, `restarted`, `reloaded`.
        * Type: String.
        * Default: `'started'`

    * `enabled`:

        * Optional. If the unit should start at boot or not.
        * Type: Bool.
        * Default: `true`

`systemd_unit__services__host_var` / `systemd_unit__services__group_var`

* List of Systemd Service Units.
* Type: List of dictionaries.
* Default: `[]`
* Subkeys:

    * `name`:

        * Mandatory. Name of the systemd service. Will be used as the filename.
        * Type: String.

    * `description`:

        * Optional. The description for the unit. If ommitted, the name will be used, suffixed by `Service`.
        * Type: String.
        * Default: unset

    * `wanted_by`:

        * Optional. Value for `WantedBy`.
        * Type: String.
        * Default: `'default.target'`

    * `raw_unit`:

        * Optional. Raw block in the `[Unit]` section.
        * Type: String.
        * Default: unset

    * `raw_service`:

        * Optional. Raw block in the `[Service]` section.
        * Type: String.
        * Default: unset

    * `raw_install`:

        * Optional. Raw block in the `[Install]` section.
        * Type: String.
        * Default: unset

    * `state`:

        * Optional. State of the unit. Possible options: `present`, `absent`, `started`, `stopped`, `restarted`, `reloaded`.
        * Type: String.
        * Default: `'started'`

    * `enabled`:

        * Optional. If the unit should start at boot or not.
        * Type: Bool.
        * Default: `true`

`systemd_unit__timers__host_var` / `systemd_unit__timers__group_var`

* List of Systemd Timer Units.
* Type: List of dictionaries.
* Default: `[]`
* Subkeys:

    * `name`:

        * Mandatory. Name of the systemd timer. Will be used as the filename.
        * Type: String.

    * `description`:

        * Optional. The description for the unit. If ommitted, the name will be used, suffixed by `Timer`.
        * Type: String.
        * Default: unset

    * `wanted_by`:

        * Optional. Value for `WantedBy`.
        * Type: String.
        * Default: `'default.target'`

    * `raw_unit`:

        * Optional. Raw block in the `[Unit]` section.
        * Type: String.
        * Default: unset

    * `raw_timer`:

        * Optional. Raw block in the `[Service]` section.
        * Type: String.
        * Default: unset

    * `raw_install`:

        * Optional. Raw block in the `[Install]` section.
        * Type: String.
        * Default: unset

    * `state`:

        * Optional. State of the unit. Possible options: `present`, `absent`, `started`, `stopped`, `restarted`, `reloaded`.
        * Type: String.
        * Default: `'started'`

    * `enabled`:

        * Optional. If the unit should start at boot or not.
        * Type: Bool.
        * Default: `true`

Example:
```yaml
# optional
systemd_unit__mounts__host_var:
  - name: 'mnt-my\x2dfolder'
    raw_mount: |-
      What=//srv1/my-share
      Where=/mnt/my-folder
      Type=cifs
      Options=credentials=/root/.smbcreds,domain=example.com,vers=default
    enabled: true
    state: 'started'

# two services, one with more options, one minimal
systemd_unit__services__host_var:
  - name: 'fwb'
    description: 'Firewall Builder'
    raw_unit: |-
      After=default.target openvpn-server@server.service fail2ban.service
    raw_service: |-
      ExecReload=/etc/fwb.sh start
      ExecStart=/etc/fwb.sh start
      ExecStop=/etc/fwb.sh stop
      RemainAfterExit=yes
      Type=oneshot
    wanted_by: 'basic.target'
    state: 'started'
    enabled: true
  - name: 'duba'
    raw_service: |-
      ExecStart=/usr/local/bin/duba
      Type=oneshot

# two timers, one with more options, one minimal
systemd_unit__timers__host_var:
  - name: 'python-venv-update@'
    description: 'python-venv update timer for /opt/python-venv/%i'
    raw_timer: |-
      OnCalendar=daily
      Unit=python-venv@%i.service
    wanted_by: 'timers.target'
    state: 'present'
    enabled: true
  - name: 'duba'
    raw_timer: |-
      OnCalendar=daily

# systemd service for a java application
systemd_unit__services__host_var:
  - name: 'myjavaapp'
    description: 'myjavaapp'
    raw_unit: |-
      After=syslog.target network.target
      Requires=network.target
    raw_service: |-
      ExecStart=/usr/bin/java -Xmx1g -XX:MaxPermSize=250M -Djava.awt.headless=true -jar /opt/myjavaapp/myjavaapp.jar 8112
      Type=simple
      User=myjavaapp
      WorkingDirectory=/opt/myjavaapp
    wanted_by: 'basic.target'
    state: 'started'
    enabled: true

```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
