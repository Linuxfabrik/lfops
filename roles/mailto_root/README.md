# Ansible Role linuxfabrik.lfops.mailto_root

This role enables relaying all mail that is sent to the root user (or other service accounts on the system) to an actual mail account. For example, any output of crontab is sent tho the configured address if this role is applied to the system.


*Available since LFOps `2.0.0`.*


## Dependent Roles

Any [LFOps playbook](https://github.com/Linuxfabrik/lfops/blob/main/playbooks/README.md) that installs this role runs these for you. Optional ones can be disabled via the playbook's skip variables.

* postfix must be installed and configured; it provides the `sendmail` interface used to send the relayed mail (role: [linuxfabrik.lfops.postfix](https://github.com/Linuxfabrik/lfops/tree/main/roles/postfix)).


## Tags

`mailto_root`

* Sends a test mail to root and to the first address in `mailto_root__to`.
* Triggers: none.
* This tag does not deploy the root aliases or the sender rewrite. The playbook passes `mailto_root__from` and `mailto_root__to` to the postfix role, which deploys them. After changing either variable, run the postfix role through a playbook that includes this role, e.g. `ansible-playbook --inventory myinv linuxfabrik.lfops.mailto_root --tags postfix,mailto_root`.


## Mandatory Role Variables

`mailto_root__from`

* The sender address from which the relayed mail should be sent.
* Type: String.

`mailto_root__to`

* List of recipient addresses to which the mails should be relayed.
* Type: List of strings.

Example:
```yaml
# mandatory
mailto_root__from: 'noreply@example.com'
mailto_root__to:
  - 'root@example.com'
  - 'root@other.example'
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
