# Ansible Role linuxfabrik.lfops.timezone

This role sets the desired timezone.

Runs on

* Fedora 35
* RHEL 7 (and compatible)
* RHEL 8 (and compatible)
* RHEL 9 (and compatible)
* Ubuntu 16


## Tags

| Tag        | What it does      |
| ---        | ------------      |
| `timezone` | Sets the timezone |


## Optional Role Variables

| Variable             | Description                                                                                                                      | Default Value     |
| --------             | -----------                                                                                                                      | -------------     |
| `timezone__timezone` | Set timezone. Have a look at the [Wikipedia List](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones) for the options. | `'Europe/Zurich'` |

Example:
```yaml
# optional
timezone__timezone: 'Europe/Zurich'
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
