# Ansible Role linuxfabrik.lfops.alternatives

This role manages symbolic links using the `update-alternatives` tool.     Useful when multiple programs are installed but provide similar functionality (for example, different editors or Python interpreters).

Hints:

* The priority is simply an integer weight that the system uses when you're in `auto` mode to choose which of several installed alternatives should be the current default.
* When you install multiple candidates for the same generic name (e.g. `python3`), and you've left the alternative in `auto` mode, the one with the highest priority number will be selected.
* When priorities are equal, the system will pick the first one that was registered (but you should avoid duplicate priorities to prevent ambiguity).


## Tags

| Tag       | What it does                         | Reload / Restart |
| ---       | ------------                         | ---------------- |
| `alternatives` | Manages alternative programs for common commands. | - |


## Mandatory Role Variables

| Variable | Description | Default Value |
| -------- | ----------- | ------------- |
| `alternatives__alternatives` | List of alternatives to remove or to deploy. Subkeys:<ul><li>`link`: String. The path to the symbolic link that should point to the real executable. This option is always required on RHEL-based distributions. On Debian-based distributions this option is required when the alternative `name` is unknown to the system.</li><li>`name`: Mandatory, string. The generic name of the link.</li><li>`path`: Optional, string. The path to the real executable that the link should point to.</li><li>`priority`: Optional, number. The priority of the alternative. If no priority is given for creation `50` is used as a fallback.</li><li>`state`: Optional, string. One of:<ul><li>`selected`: Default. Install the alternative (if not already installed), and set it as the currently selected alternative for the group.</li><li>`present`: Install the alternative (if not already installed), but do not set it as the currently selected alternative for the group.</li><li>`auto`: Install the alternative (if not already installed), and set the group to auto mode.</li><li>`absent`: Remove the alternative.</li></ul></ul> | `[]` |

Example:
```yaml
alternatives__alternatives:
  - link: '/usr/bin/python3'
    name: 'python3'
    path: '/usr/bin/python3.9'
    priority: '100'  # install python3.9 with higher priority
    state: 'auto'
  - link: '/usr/bin/python3'
    name: 'python3'
    path: '/usr/bin/python3.12'
    priority: '10'
    state: 'auto'
# => results in python3.9
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
