# Ansible Role redis

This role installs and configures [Redis](https://redis.io/), per default listening on TCP 127.0.0.1:6379. Note that this role configures Systemd with unit file overrides for Redis.

This role is only compatible with Redis versions

* 5
* 6

FQCN: linuxfabrik.lfops.redis

Tested on

* RHEL 8 (and compatible)


## Requirements

### Mandatory

This role does not have any mandatory requirements.


### Optional

This role does not have any optional requirements.


## Tags

| Tag                  | What it does                                  |
| ---                  | ------------                                  |
| redis                | Installs and configures Redis                 |
| redis:state          | Manages the state of the Redis service        |


## Role Variables

Have a look at the [defaults/main.yml](https://github.com/Linuxfabrik/lfops/blob/main/roles/redis/defaults/main.yml) for the variable defaults.


### Mandatory

This role does not have any mandatory variables.


### Optional

#### redis__conf_* config directives

Variables for `redis.conf` directives and their default values, defined and supported by this role.

| Role Variable                             | Default                               | Documentation                                                         |
|---------------                            |---------                              |---------------                                                        |
| redis__conf_auto_aof_rewrite_min_size     | '64mb'                                | [redis.conf](https://github.com/redis/redis/blob/6.0/redis.conf) |
| redis__conf_bind                          | '127.0.0.1'                           | [redis.conf](https://github.com/redis/redis/blob/6.0/redis.conf) |
| redis__conf_daemonize                     | 'no'                                  | [redis.conf](https://github.com/redis/redis/blob/6.0/redis.conf) |
| redis__conf_databases                     | 16                                    | [redis.conf](https://github.com/redis/redis/blob/6.0/redis.conf) |
| redis__conf_loglevel                      | 'notice'                              | [redis.conf](https://github.com/redis/redis/blob/6.0/redis.conf) |
| redis__conf_maxmemory                     | '50mb'                                | [redis.conf](https://github.com/redis/redis/blob/6.0/redis.conf) |
| redis__conf_maxmemory_policy              | 'noeviction'                          | [redis.conf](https://github.com/redis/redis/blob/6.0/redis.conf) |
| redis__conf_port                          | 6379                                  | [redis.conf](https://github.com/redis/redis/blob/6.0/redis.conf) |
| redis__conf_protected_mode                | 'yes'                                 | [redis.conf](https://github.com/redis/redis/blob/6.0/redis.conf) |
| redis__conf_replica_serve_stale_data      | 'yes'                                 | [redis.conf](https://github.com/redis/redis/blob/6.0/redis.conf) |
| redis__conf_supervised                    | 'auto'                                | [redis.conf](https://github.com/redis/redis/blob/6.0/redis.conf) |


#### redis__installed_version

Installs the specified Redis version.

Default:
```yaml
redis__installed_version: 6
```


#### redis__service_enabled

Enables or disables the influxdb service, analogous to `systemctl enable/disable --now`. Possible options:
* true
* false

Default:
```yaml
redis__service_enabled: true
```


#### redis__service_limit_nofile

Systemd: Resource limit directive for the number of file descriptors.

Default:
```yaml
redis__service_limit_nofile: 10240
```


#### redis__service_timeout_start_sec

Systemd: Configures the time to wait for start-up. If Redis does not signal start-up completion within the configured time, the service will be considered failed and will be shut down again.

Default:
```yaml
redis__service_timeout_start_sec: 5
```


#### redis__service_timeout_stop_sec

Systemd: First, it configures the time to wait for the ExecStop= command. Second, it configures the time to wait for the Redis itself to stop. If Redis doesn't terminate in the specified time, it will be forcibly terminated by SIGKILL.

Default:
```yaml
redis__service_timeout_stop_sec: 5
```


## Known Issues

Actually not an issue: The role configures Systemd correctly, even if you get `WARNING supervised by systemd - you MUST set appropriate values for TimeoutStartSec and TimeoutStopSec in your service unit` in `/var/log/redis/redis.log`. This can safely be ignored [according to this GitHub issue](https://github.com/redis/redis/issues/8024).



## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
