# Ansible Role linuxfabrik.lfops.tmux

This role installs [tmux](https://github.com/tmux/tmux) and deploys a system-wide `/etc/tmux.conf` with sensible defaults, for example a larger scrollback buffer.


*Available in the next LFOps release.*


## How the Role Behaves

* The configuration is fully templated. On every run `/etc/tmux.conf` is re-rendered from the role's template (a timestamped backup is kept), so out-of-band manual edits are overwritten. Manage all settings through the role variables below.
* A changed configuration takes effect for newly started tmux sessions. Already running sessions keep their loaded configuration until they are restarted or the file is sourced manually.
* Copy-mode selections are sent to the clipboard of the local terminal emulator through the OSC 52 escape sequence (`set-clipboard on`). This works over SSH, but only if the local terminal emulator supports OSC 52. Terminals without OSC 52 support simply ignore the sequence.
* As a terminal-independent alternative, `prefix + P` writes the complete scrollback buffer of the current pane to `/tmp/tmux-scrollback-<user>-<session>-<window>.<pane>.txt` (mode `0600`, since the scrollback may contain secrets). From there it can be copied off the host, searched or archived. A confirmation with the exact path is shown in the status line.


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


## Troubleshooting

**Copy mode does not reach the local clipboard over SSH**

* OSC 52 (`set-clipboard on`) hands the selection to the *local* terminal emulator, which this role cannot configure. The emulator must support and allow OSC 52 clipboard writes. foot, kitty, WezTerm and Alacritty work out of the box. xterm needs `XTerm*disallowedWindowOps: 20,21,SetXprop` in `~/.Xresources` (OSC 52 is disabled by default there). gnome-terminal and other VTE terminals only support OSC 52 from VTE 0.78 onwards.
* Note that the relevant terminal is the one running *locally*. Over SSH the remote-only tools `wl-copy` / `xclip` cannot reach your local clipboard; OSC 52 is what carries the data back through the connection.
* Independent of any terminal support, `prefix + P` dumps the whole scrollback to a file (see [How the Role Behaves](#how-the-role-behaves)) that can be copied off the host.

**Clipboard does not work through nested tmux (tmux inside tmux)**

* Each tmux layer relays the OSC 52 of an inner tmux only when its own `set-clipboard` is `on`; the tmux default `external` sets the clipboard from its own copy mode but swallows OSC 52 coming from an inner tmux. Set `set-clipboard on` in any outer tmux you manage yourself, for example a local `~/.tmux.conf`.

**Copied text pastes with middle-click but not with Ctrl+V**

* The terminal stored the OSC 52 data in the PRIMARY selection (middle-click) instead of CLIPBOARD (Ctrl+V). tmux sends an empty selection target and terminals differ in how they interpret it. On xterm, add `XTerm*selectToClipboard: true` to `~/.Xresources` to route it to CLIPBOARD.

**`missing or unsuitable terminal: <name>` when starting tmux over SSH**

* The remote host has no terminfo entry for your local terminal (common with `foot` and `xterm-kitty`). This is a terminfo gap, not a role problem. Either connect with a `TERM` the host already knows, for example `TERM=xterm-256color ssh <host>`, or copy your terminfo to the host once with `infocmp -x | ssh <host> tic -x -`.


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
