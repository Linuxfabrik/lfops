# Ansible Role linuxfabrik.lfops.mailx

This role installs [mailx](http://heirloom.sourceforge.net/mailx.html) and deploys a bash wrapper script that makes sending mail easier to `/root/send-mail`.


## Tags

`mailx`

* Installs the mailx package.
* Deploys a bash wrapper script to `/root/send-mail`.
* Triggers: none.


## Skip Variables

This role is used in several playbooks that provide skip variables to disable specific dependencies. See the playbooks documentation for details:

* [mailto_root.yml](https://github.com/Linuxfabrik/lfops/blob/main/playbooks/README.md#mailto_rootyml)
* [postfix.yml](https://github.com/Linuxfabrik/lfops/blob/main/playbooks/README.md#postfixyml)
* [setup_basic.yml](https://github.com/Linuxfabrik/lfops/blob/main/playbooks/README.md#setup_basicyml)
* [system_update.yml](https://github.com/Linuxfabrik/lfops/blob/main/playbooks/README.md#system_updateyml)


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
