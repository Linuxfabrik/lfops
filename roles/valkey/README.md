# Ansible Role linuxfabrik.lfops.valkey

This role installs and configures [Valkey](https://valkey.io/), per default listening on TCP 127.0.0.1:6379. Note that this role configures systemd with unit file overrides for Valkey.

Valkey is installed from the distribution repositories. Which version that is depends on the operating system.

Debian 12 and Ubuntu 22.04 do not ship Valkey and are therefore not supported. Use the [linuxfabrik.lfops.redis](https://github.com/Linuxfabrik/lfops/tree/main/roles/redis) role there.

This role is compatible with the following Valkey versions:

* 7.2
* 8.0
* 8.1
* 9.0


*Available in the next LFOps release.*


## How the Role Behaves

* The role does not pin a Valkey version. It installs whatever the enabled repositories offer, reads the installed version back from the package database, and deploys the configuration template matching that version. If no template matches, the run aborts with the list of supported versions instead of failing on a missing file.
* The whole configuration file is templated, so local edits to `/etc/valkey/valkey.conf` are overwritten on the next run. A backup of the previous file is kept next to it.
* The role manages TCP access only. The unix socket the RHEL packages enable by default is commented out in the deployed configuration.
* On RHEL 10 there is no Redis in the distribution repositories, so this role is the drop-in replacement for [linuxfabrik.lfops.redis](https://github.com/Linuxfabrik/lfops/tree/main/roles/redis) there. Valkey and Redis both listen on TCP 6379 by default, so do not run both roles against the same host without changing one of the ports.


## Tags

`valkey`

* Installs and configures Valkey.
* Triggers: valkey.service restart.

`valkey:state`

* Manages the state of the Valkey service.
* Triggers: none.


## Optional Role Variables

`valkey__service_enabled`

* Enables or disables the valkey service, analogous to `systemctl enable/disable`.
* Type: Bool.
* Default: `true`

`valkey__service_limit_nofile`

* Systemd: Resource limit directive for the number of file descriptors.
* Type: Number.
* Default: `10240`
* Deviates from the upstream default on Debian and Ubuntu, whose unit sets `65535`, and matches it on RHEL, whose unit sets `10240`: one value across all platforms keeps the descriptor budget of a host predictable, and 10240 covers the default `maxclients` of 10000 plus the server's own descriptors.

`valkey__service_state`

* Changes the state of the valkey service, analogous to `systemctl start/stop/restart/reload`.
* Type: String. One of `reloaded`, `restarted`, `started`, `stopped`.
* Default: `'started'` if `valkey__service_enabled` is `true`, else `'stopped'`

`valkey__service_timeout_start_sec`

* Systemd: Configures the time to wait for start-up. If Valkey does not signal start-up completion within the configured time, the service will be considered failed and will be shut down again.
* Type: String.
* Default: `'90s'`

`valkey__service_timeout_stop_sec`

* Systemd: First, it configures the time to wait for the ExecStop= command. Second, it configures the time to wait for Valkey itself to stop. If Valkey doesn't terminate in the specified time, it will be forcibly terminated by SIGKILL.
* Type: String.
* Default: `'90s'`
* Deviates from the upstream default on Debian and Ubuntu, whose unit sets `TimeoutStopSec=0` and therefore waits indefinitely: a shutdown that hangs on a large dataset blocks a reboot forever instead of being cut short. On RHEL the unit leaves the setting commented out, where systemd's own default is the same 90s.

Example:

```yaml
# optional
valkey__service_enabled: true
valkey__service_limit_nofile: 10240
valkey__service_state: 'started'
valkey__service_timeout_start_sec: 5
valkey__service_timeout_stop_sec: 5
```


## Optional Role Variables - `valkey__conf_*` Config Directives

Variables for `valkey.conf` directives and their default values, defined and supported by this role.

`valkey__conf_appendonly`

* [valkey.conf](https://github.com/valkey-io/valkey/blob/8.0/valkey.conf)
* Type: String.
* Default: `'no'`

`valkey__conf_auto_aof_rewrite_min_size`

* [valkey.conf](https://github.com/valkey-io/valkey/blob/8.0/valkey.conf)
* Type: String.
* Default: `'64mb'`

`valkey__conf_bind`

* [valkey.conf](https://github.com/valkey-io/valkey/blob/8.0/valkey.conf)
* Type: String.
* Default: `'127.0.0.1'`

`valkey__conf_daemonize`

* [valkey.conf](https://github.com/valkey-io/valkey/blob/8.0/valkey.conf)
* Type: String.
* Default: `'no'`

`valkey__conf_databases`

* [valkey.conf](https://github.com/valkey-io/valkey/blob/8.0/valkey.conf)
* Type: Number.
* Default: `16`

`valkey__conf_loglevel`

* [valkey.conf](https://github.com/valkey-io/valkey/blob/8.0/valkey.conf)
* Type: String.
* Default: `'notice'`

`valkey__conf_maxmemory`

* [valkey.conf](https://github.com/valkey-io/valkey/blob/8.0/valkey.conf)
* Type: String.
* Default: `'50M'`
* Deviates from the upstream default `0`, which lets the dataset grow until the host runs out of memory: a cache that is bounded by default cannot take the rest of the host down with it. Raise it to what the application actually needs, and note that `valkey__conf_maxmemory_policy` is `noeviction`, so reaching the limit makes writes fail rather than evicting keys.

`valkey__conf_maxmemory_policy`

* [valkey.conf](https://github.com/valkey-io/valkey/blob/8.0/valkey.conf)
* Type: String.
* Default: `'noeviction'`

`valkey__conf_port`

* If port `0` is specified Valkey will not listen on a TCP socket. [valkey.conf](https://github.com/valkey-io/valkey/blob/8.0/valkey.conf)
* Type: Number.
* Default: `6379`

`valkey__conf_protected_mode`

* [valkey.conf](https://github.com/valkey-io/valkey/blob/8.0/valkey.conf)
* Type: String.
* Default: `'yes'`

`valkey__conf_replica_serve_stale_data`

* [valkey.conf](https://github.com/valkey-io/valkey/blob/8.0/valkey.conf)
* Type: String.
* Default: `'yes'`

`valkey__conf_requirepass`

* [valkey.conf](https://github.com/valkey-io/valkey/blob/8.0/valkey.conf)
* Type: String.
* Default: unset

`valkey__conf_save`

* [valkey.conf](https://github.com/valkey-io/valkey/blob/8.0/valkey.conf)
* Type: List.
* Default: `['3600 1', '300 100', '60 10000']`

`valkey__conf_supervised`

* [valkey.conf](https://github.com/valkey-io/valkey/blob/8.0/valkey.conf)
* Type: String.
* Default: `'auto'`

`valkey__conf_tls_auth_clients`

* [valkey.conf](https://github.com/valkey-io/valkey/blob/8.0/valkey.conf)
* Type: String.
* Default: unset

`valkey__conf_tls_ca_cert_file`

* [valkey.conf](https://github.com/valkey-io/valkey/blob/8.0/valkey.conf)
* Type: String.
* Default: unset

`valkey__conf_tls_cert_file`

* [valkey.conf](https://github.com/valkey-io/valkey/blob/8.0/valkey.conf)
* Type: String.
* Default: unset

`valkey__conf_tls_key_file`

* [valkey.conf](https://github.com/valkey-io/valkey/blob/8.0/valkey.conf)
* Type: String.
* Default: unset

`valkey__conf_tls_port`

* TLS Port. Set `valkey__conf_port: 0` to only listen with TLS. [valkey.conf](https://github.com/valkey-io/valkey/blob/8.0/valkey.conf)
* Type: Number.
* Default: unset

Example:

```yaml
valkey__conf_appendonly: 'yes'
valkey__conf_auto_aof_rewrite_min_size: '64mb'
valkey__conf_bind: '127.0.0.1'
valkey__conf_daemonize: 'no'
valkey__conf_databases: 16
valkey__conf_loglevel: 'notice'
valkey__conf_maxmemory: '50M'
valkey__conf_maxmemory_policy: 'noeviction'
valkey__conf_port: 6379  # If port 0 is specified Valkey will not listen on a TCP socket.
valkey__conf_protected_mode: 'yes'
valkey__conf_replica_serve_stale_data: 'yes'
valkey__conf_requirepass: 'linuxfabrik'
valkey__conf_save:
  - '3600 1'
  - '300 100'
  - '60 10000'
valkey__conf_tls_auth_clients: 'no'
valkey__conf_tls_ca_cert_file: '/etc/valkey/ca.pem'
valkey__conf_tls_cert_file: '/etc/valkey/valkey.pem'
valkey__conf_tls_key_file: '/etc/valkey/valkey.key'
valkey__conf_tls_port: 6379
valkey__conf_supervised: 'auto'
```


## Troubleshooting

**The run aborts with `Valkey X.Y is not supported by this role`**

* The enabled repositories offer a Valkey version this role has no configuration template for. Either pin the host to a supported version, or add the matching `roles/valkey/templates/etc/valkey/<version>-valkey.conf.j2` template.

**`WARNING supervised by systemd - you MUST set appropriate values for TimeoutStartSec and TimeoutStopSec in your service unit` in the Valkey log**

* Not really a problem: the role configures systemd correctly. This can be safely ignored [according to this GitHub issue](https://github.com/redis/redis/issues/8024).


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
