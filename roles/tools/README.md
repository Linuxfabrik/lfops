# Ansible Role linuxfabrik.lfops.tools

This role ensures that some additional tools are installed and the Bash environment is configured.

Tools that this role installs:

* bash-completion
* lsof
* nano
* rsync
* tmux
* vim
* wget

This role sets some new Bash alias for:

* dmesg
* poweroff
* reboot
* whatismyip

Bash:

* export EDITOR
* HISTSIZE=100000
* HISTTIMEFORMAT="%Y-%m-%d %T $USER $SUDO_USER "
* Colorizes the Bash prompt and sets it to something like `[17:30:19 user@server Rocky8 ~]$ `

Tested on

* Fedora
* RHEL 7 (and compatible)
* RHEL 8 (and compatible)


## Mandatory Requirements

* On RHEL-compatible systems, enable the EPEL repository. This can be done using the [linuxfabrik.lfops.repo_epel](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_epel) role.


## Tags

| Tag     | What it does                       |
| ---     | ------------                       |
| `tools` | Installs and configures some tools |


## Optional Role Variables

| Variable            | Description                                                                  | Default Value                                                                                                                                                           |
| --------            | -----------                                                                  | -------------                                                                                                                                                           |
| `tools__editor`     | Set the standard editor, for example for editing crontabs.                   | `'nano'`                                                                                                                                                                |
| `tools__prompt_ps1` | Set a custom primary prompt for bash. This is displayed before each command. | * green, if the host is in an Ansible group called `test`<br> * yellow, if the host is in an Ansible group called `stage`<br> * red, if neither condition above applies, assuming a productive machine |

Example:
```yaml
# optional
tools__editor: 'vim'
tools__prompt_ps1: '[\[\033[0;34m\]\$(date +%H:%M:%S) \u@\h \w$NO_COLOR]\$ '
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
