# Ansible Role linuxfabrik.lfops.timezone

This role sets the system timezone (the `/etc/localtime` symlink, which `date`, system logs, cron jobs and journald all use) via the `community.general.timezone` module.


*Available since LFOps `2.0.0`.*


## Tags

`timezone`

* Sets the timezone.
* Triggers: none.


## Optional Role Variables

`timezone__timezone`

* Set timezone. Have a look at the [Wikipedia List](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones) for the options.
* Type: String.
* Default: `'Europe/Zurich'`

Example:
```yaml
# optional
timezone__timezone: 'Europe/Zurich'
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
