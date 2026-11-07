# Ansible Role linuxfabrik.lfops.dnf

This role sets options in the `[main]` section of the DNF configuration, `/etc/dnf/dnf.conf`. By default it only makes DNF drop a slow mirror sooner. The `setup_basic` playbook runs it on every host; where the package manager is not DNF 4 (`ansible_facts["pkg_mgr"]` is not `dnf`, as on Debian, Ubuntu and Fedora 41 and newer), it does nothing.

The role edits the file in place with `community.general.ini_file` instead of deploying a template like most LFOps roles. Only the listed options change, settings added by hand such as `proxy=` or `exclude=` stay, and the file carries no `ansible_managed` header.


*Available in the next LFOps release.*


## How the Role Behaves

* Options the role does not list, including the ones RHEL ships such as `gpgcheck` or `installonly_limit`, stay as they are. To remove an option, also one set by hand, list it with `state: 'absent'`.
* DNF reads `dnf.conf` on every call, so there is no service to restart. An option set in a `.repo` file overrides the one in `[main]` for that repository.


## Tags

`dnf`

* Sets the options in `/etc/dnf/dnf.conf`.
* Triggers: none.

`dnf:configure`

* Sets the options in `/etc/dnf/dnf.conf`.
* Triggers: none.


## Optional Role Variables

`dnf__conf_options__host_var` / `dnf__conf_options__group_var`

* Options for the `[main]` section of `/etc/dnf/dnf.conf`. An entry with the same `name` overrides the one of a lower level, including the role defaults. For the options and their values, see `man 5 dnf.conf` or the [DNF Configuration Reference](https://dnf.readthedocs.io/en/latest/conf_ref.html). The role checks the formats of `installonly_limit`, `minrate` and `timeout` before it writes the file, since DNF only logs an invalid value and falls back to its built-in default.
* Type: List of dictionaries.
* Default:

    ```yaml
    - name: 'minrate'
      value: '200k'
    - name: 'timeout'
      value: '15'
    ```

* Deviates from the upstream defaults `minrate=1000` and `timeout=30`: DNF aborts a transfer that is slower than `minrate` bytes per second for `timeout` seconds and moves on to the next mirror, while with the upstream values it stays on a mirror that delivers a few dozen kilobytes per second and takes minutes for the metadata of a single repository. A host whose link is slower than 200 KB/s needs a lower `minrate`.
* Subkeys:

    * `name`:

        * Mandatory. Name of the option, for example `proxy`.
        * Type: String.

    * `value`:

        * Mandatory unless `state` is `absent`. Value of the option, written as it is.
        * Type: String or Number.

    * `state`:

        * Optional. Whether the option is set in or removed from `/etc/dnf/dnf.conf`. One of `present` or `absent`.
        * Type: String.
        * Default: `'present'`

Example:
```yaml
# optional
dnf__conf_options__host_var:
  - name: 'proxy'
    value: 'http://proxy.example.com:3128'
  - name: 'timeout'
    value: '30'
  - name: 'exclude'
    state: 'absent'
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
