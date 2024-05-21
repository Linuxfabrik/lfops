# Ansible Role linuxfabrik.lfops.redis

This role installs and configures [Redis](https://redis.io/), per default listening on TCP 127.0.0.1:6379. Note that this role configures Systemd with unit file overrides for Redis.

This role is compatible with Redis v5+.

You can pre-enable Remi's repo with the [linuxfabrik.lfops.repo_remi](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_remi) role to get an up-to-date Redis version. If you use the [Redis Playbook](https://github.com/Linuxfabrik/lfops/blob/main/playbooks/redis.yml), this is automatically done for you.


## Tags

| Tag           | What it does                           |
| ---           | ------------                           |
| `redis`       | Installs and configures Redis          |
| `redis:state` | Manages the state of the Redis service |


## Optional Role Variables

| Variable | Description | Default Value |
| -------- | ----------- | ------------- |
| `redis__service_enabled` | Enables or disables the redis service, analogous to `systemctl enable/disable --now`. | `true` |
| `redis__service_limit_nofile` | Systemd: Resource limit directive for the number of file descriptors. | `10240` |
| `redis__service_timeout_start_sec` | Systemd: Configures the time to wait for start-up. If Redis does not signal start-up completion within the configured time, the service will be considered failed and will be shut down again. | `'90s'` |
| `redis__service_timeout_stop_sec` | Systemd: First, it configures the time to wait for the ExecStop= command. Second, it configures the time to wait for the Redis itself to stop. If Redis doesn't terminate in the specified time, it will be forcibly terminated by SIGKILL. | `'90s'` |

Example:
```yaml
# optional
redis__service_enabled: true
redis__service_limit_nofile: 10240
redis__service_timeout_start_sec: 5
redis__service_timeout_stop_sec: 5
```


### `redis__conf_*` config directives

Variables for `redis.conf` directives and their default values, defined and supported by this role.

| Role Variable                           | Documentation                                                    | Default Value  |
| -------------                           | -------------                                                    | -------------  |
| `redis__conf_appendonly`                | [redis.conf](https://github.com/redis/redis/blob/7.2/redis.conf) | `'no'`         |
| `redis__conf_auto_aof_rewrite_min_size` | [redis.conf](https://github.com/redis/redis/blob/7.2/redis.conf) | `'64mb'`       |
| `redis__conf_bind`                      | [redis.conf](https://github.com/redis/redis/blob/7.2/redis.conf) | `'127.0.0.1'`  |
| `redis__conf_daemonize`                 | [redis.conf](https://github.com/redis/redis/blob/7.2/redis.conf) | `'no'`         |
| `redis__conf_databases`                 | [redis.conf](https://github.com/redis/redis/blob/7.2/redis.conf) | `16`           |
| `redis__conf_loglevel`                  | [redis.conf](https://github.com/redis/redis/blob/7.2/redis.conf) | `'notice'`     |
| `redis__conf_maxmemory`                 | [redis.conf](https://github.com/redis/redis/blob/7.2/redis.conf) | `'50M'`       |
| `redis__conf_maxmemory_policy`          | [redis.conf](https://github.com/redis/redis/blob/7.2/redis.conf) | `'noeviction'` |
| `redis__conf_port`                      | If port `0` is specified Redis will not listen on a TCP socket. [redis.conf](https://github.com/redis/redis/blob/7.2/redis.conf) | `6379`         |
| `redis__conf_protected_mode`            | [redis.conf](https://github.com/redis/redis/blob/7.2/redis.conf) | `'yes'`        |
| `redis__conf_replica_serve_stale_data`  | [redis.conf](https://github.com/redis/redis/blob/7.2/redis.conf) | `'yes'`        |
| `redis__conf_requirepass`               | [redis.conf](https://github.com/redis/redis/blob/7.2/redis.conf) | `unset`        |
| `redis__conf_save`                      | [redis.conf](https://github.com/redis/redis/blob/7.2/redis.conf) | v5: `['900 1', '300 10', '60 10000']`<br>v6: `['3600 1', '300 100', '60 10000']`<br>v7: `['3600 1', '300 100', '60 10000']` |
| `redis__conf_supervised`                | [redis.conf](https://github.com/redis/redis/blob/7.2/redis.conf) | `'no'`       |

Example:

```yaml
redis__conf_appendonly: 'yes'
redis__conf_auto_aof_rewrite_min_size: '64mb'
redis__conf_bind: '127.0.0.1'
redis__conf_daemonize: 'no'
redis__conf_databases: 16
redis__conf_loglevel: 'notice'
redis__conf_maxmemory: '50M'
redis__conf_maxmemory_policy: 'noeviction'
redis__conf_port: 6379  # If port 0 is specified Redis will not listen on a TCP socket.
redis__conf_protected_mode: 'yes'
redis__conf_replica_serve_stale_data: 'yes'
redis__conf_requirepass: 'password'
redis__conf_save:
  - '3600 1'
  - '300 100'
  - '60 10000'
redis__conf_supervised: 'auto'
```


## Troubleshooting

Not really a problem: The role configures systemd correctly, even if you get `WARNING supervised by systemd - you MUST set appropriate values for TimeoutStartSec and TimeoutStopSec in your service unit' in `/var/log/redis/redis.log`. This can be safely ignored [according to this GitHub issue](https://github.com/redis/redis/issues/8024).


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
