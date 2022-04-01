# Ansible Role tools

This role ensures that some additional tools are installed and the Bash environment is configured.

Tools that this role installs:

* bash-completion
* lsof
* nano
* rsync
* tmux
* vim
* wget

This role sets some alias's:

* dmesg
* lf-confirm
* poweroff
* reboot
* reboot
* schedule-icinga-downtime
* whatismyip

Bash:

* export EDITOR
* HISTSIZE=100000
* HISTTIMEFORMAT="%Y-%m-%d %T $USER $SUDO_USER "
* Customizes the Bash prompt

FQCN: linuxfabrik.lfops.tools

Tested on

* Fedora
* RHEL 7 (and compatible)
* RHEL 8 (and compatible)


## Requirements

### Mandatory

* On RHEL-compatible systems, enable the EPEL repository. This can be done using the [linuxfabrik.lfops.repo_epel](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_epel) role.


### Optional

This role does not have any optional requirements.


## Tags

| Tag   | What it does                       |
| ---   | ------------                       |
| tools | Installs and configures some tools |


## Role Variables

Have a look at the [defaults/main.yml](https://github.com/Linuxfabrik/lfops/blob/main/roles/tools/defaults/main.yml) for the variable defaults.


### Mandatory

This role does not have any mandatory variables.


### Optional

#### tools__editor

Set the standard editor, for example for editing crontabs.

Default:
```yaml
tools__editor: 'nano'
```

#### tools__prompt_ps1

Set a custom primary prompt for bash. This is displayed before each command. Defaults to:

* green, if the host is in an Ansible group called `test`
* yellow, if the host is in an Ansible group called `stage`
* red, if neither condition above applies

Example:
```yaml
tools__prompt_ps1: '[\[\033[0;34m\]\$(date +%H:%M:%S) \u@\h \w$NO_COLOR]\$ '
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
