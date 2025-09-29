# Ansible Role linuxfabrik.lfops.blocky

This role installs and configures blocky, a DNS proxy and ad-blocker for the local network written in Go.

This Ansible role does not provide a way to template the blocky configuration file – it is simply far too dynamic. Also it does not currently support multiple blocky instances synchronizing their caches and locking state via redis. If you have multiple instances, just deploy the same config.yml to a group of blocky instances, and you will be fine.


## Tags

| Tag                | What it does                                 | Reload / Restart |
| ---                | ------------                                 | ---------------- |
| `blocky`           | Downloads blocky from GitHub to the Ansible control node, copies it to the remote host, configures Systemd, applies a default configuration, and overrides it with a custom configuration (if available). | Restarts blocky.service |
| `blocky:configure` | Copies and applies a custom blocky configuration file. | Restarts blocky.service |
| `blocky:state`     | Enable/disable the default blocky service. | - |


## Optional Role Variables

| Variable | Description | Default Value |
| -------- | ----------- | ------------- |
| `blocky__config_yml`      | String. The config YAML for blocky to deploy. | unset |
| `blocky__service_enabled` | Bool. Enables or disables the service, analogous to `systemctl enable/disable --now`. | `true` |
| `blocky__version`         | String. The version of blocky to install. Possible options: `'latest'`, or any from https://github.com/0xERR0R/blocky/releases. | `'latest'` |

Example:
```yaml
# optional
blocky__config_yml: '{{ lookup("ansible.builtin.file",
    "{{ inventory_dir }}/group_vars/blocky/files/etc/blocky/config.yml")
  }}'  # example of how to deploy the config as a file
blocky__service_enabled: true
blocky__version: 'latest'
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
