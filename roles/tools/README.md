# Ansible Role linuxfabrik.lfops.tools

This role ensures that some additional tools are installed and the Bash environment is configured.

Tools that this role installs:

* bash-completion
* cloud-guest-utils on Debian, cloud-utils-growpart on RHEL
* jq
* lsof
* nano
* rsync
* sudo
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


## Mandatory Requirements

* On RHEL-compatible systems, enable the EPEL repository. This can be done using the [linuxfabrik.lfops.repo_epel](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_epel) role.


## Tags

`tools`

* Installs and configures some tools.
* Triggers: none.


## Optional Role Variables

`tools__editor`

* Set the standard editor, for example for editing crontabs.
* Type: String.
* Default: `'nano'`

`tools__icinga2_api_url`

* The URL of the Icinga2 API (usually on the Icinga2 Master). This will be used to set a downtime for the corresponding host and all its services in the `reboot` alias.
* Type: String.
* Default: `'https://{{ icinga2_agent__icinga2_master_host | d("") }}:{{ icinga2_agent__icinga2_master_port | d(5665) }}'`

`tools__icinga2_api_user_login`

* The Icinga2 API User to set the downtime for the corresponding host and all its services in the `reboot` alias.
* Type: Dictionary.
* Default: unset

`tools__icinga2_hostname`

* The hostname of the Icinga2 host on which the downtime should be set.
* Type: String.
* Default: `'{{ ansible_facts["nodename"] }}'`

`tools__prompt_ps1`

* Set a custom primary prompt for bash. This is displayed before each command.
* Type: String.
* Default: green, if the host is in an Ansible group called `test`; yellow, if the host is in an Ansible group called `stage`; red, if neither condition above applies, assuming a productive machine.

`tools__prompt_use_fqdn`

* Set to `true` to show the FQDN in the prompt.
* Type: Bool.
* Default: `false`

Example:

```yaml
# optional
tools__editor: 'vim'
tools__icinga2_api_url: 'https://icinga.example.com:5665'
tools__icinga2_api_user_login:
  username: 'downtime-user'
  password: 'linuxfabrik'
tools__icinga2_hostname: 'myhost.example.com'
tools__prompt_ps1: '[\[\033[0;34m\]\$(date +%H:%M:%S) \u@\h \w$NO_COLOR]\$ '
tools__prompt_use_fqdn: true
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
