# Ansible Role linuxfabrik.lfops.tmux

This role installs [tmux](https://github.com/tmux/tmux) and deploys a system-wide `/etc/tmux.conf` with sensible defaults, for example a larger scrollback buffer.


*Available in the next LFOps release.*


## How the Role Behaves

* The configuration is fully templated. On every run `/etc/tmux.conf` is re-rendered from the role's template (a timestamped backup is kept), so out-of-band manual edits are overwritten. Manage all settings through the role variables below.
* A changed configuration takes effect for newly started tmux sessions. Already running sessions keep their loaded configuration until they are restarted or the file is sourced manually.


## Tags

`tmux`

* Installs tmux and deploys the configuration.
* Triggers: none.


## Optional Role Variables

`tmux__history_limit`

* Maximum number of lines kept in the scrollback buffer per pane.
* Type: Number.
* Default: `100000`

`tmux__mouse`

* Enable mouse support (scroll, select and resize panes/windows).
* Type: Bool.
* Default: `true`

Example:
```yaml
# optional
tmux__history_limit: 50000
tmux__mouse: false
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
