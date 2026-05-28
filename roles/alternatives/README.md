# Ansible Role linuxfabrik.lfops.alternatives

This role manages symbolic links using the `update-alternatives` tool. Useful when multiple programs are installed but provide similar functionality (for example, different editors or Python interpreters).

Hints:

* The priority is simply an integer weight that the system uses when you're in `auto` mode to choose which of several installed alternatives should be the current default.
* When you install multiple candidates for the same generic name (e.g. `python3`), and you've left the alternative in `auto` mode, the one with the highest priority number will be selected.
* When priorities are equal, the system will pick the first one that was registered (but you should avoid duplicate priorities to prevent ambiguity).


*Available since LFOps `3.0.0`.*


## How the Role Behaves

* The role ensures the alternatives tooling is installed: the `chkconfig` package on RHEL 8, the `alternatives` package on RHEL 9 and 10. On Debian and Ubuntu, `update-alternatives` ships with `dpkg`, so nothing is installed there.
* On Red Hat-family hosts `link` is mandatory for each entry. On Debian-based hosts it is only required when the alternative `name` is unknown to the system.
* `family` is only available on Red Hat-family hosts (community.general 10.1.0+); `subcommands` requires community.general 5.1.0+. Both are passed through only when set, so they do not affect entries or platforms that do not use them.


## Tags

`alternatives`

* Installs the alternatives tooling and manages alternative programs for common commands.
* Triggers: none.


## Optional Role Variables

`alternatives__alternatives`

* List of alternatives to remove or to deploy. With the default empty list, the role is a no-op.
* Type: List of dictionaries.
* Default: `[]`
* Subkeys:

    * `name`:

        * Mandatory. The generic name of the link.
        * Type: String.

    * `family`:

        * Optional. Groups similar alternatives. Red Hat-family only.
        * Type: String.

    * `link`:

        * The path to the symbolic link that should point to the real executable. This option is always required on RHEL-based distributions. On Debian-based distributions this option is required when the alternative `name` is unknown to the system.
        * Type: String.

    * `path`:

        * Optional. The path to the real executable that the link should point to.
        * Type: String.

    * `priority`:

        * Optional. The priority of the alternative. If no priority is given, the `alternatives` tool uses `50` as a fallback on creation.
        * Type: Number.

    * `state`:

        * Optional. One of: `selected` (default; install the alternative and set it as the currently selected alternative for the group), `present` (install the alternative but do not set it as the currently selected alternative for the group), `auto` (install the alternative and set the group to auto mode), `absent` (remove the alternative).
        * Type: String.
        * Default: `'selected'`

    * `subcommands`:

        * Optional. Subcommands (also called slaves or followers) that are switched together with this alternative. Each entry needs `name`, `link`, and `path`.
        * Type: List of dictionaries.

Example:
```yaml
alternatives__alternatives:
  # set the default python3, also switching its subcommands (slaves)
  - name: 'python3'
    link: '/usr/bin/python3'
    path: '/usr/bin/python3.12'
    priority: 100
    state: 'auto'
    subcommands:
      - name: 'python3-config'
        link: '/usr/bin/python3-config'
        path: '/usr/bin/python3.12-config'
  # Red Hat-family only: select an alternative by family
  - name: 'java'
    family: 'java-11-openjdk.x86_64'
  # remove an alternative
  - name: 'editor'
    path: '/usr/bin/vim'
    state: 'absent'
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
