# Ansible Role linuxfabrik.lfops.repo_linuxfabrik

This role deploys the [Linuxfabrik package repository](https://repo.linuxfabrik.ch/), which serves the packages Linuxfabrik builds, for example FirewallFabrik and Glances. The repository has two channels: `release`, which is enabled, and `testing`, which is configured but disabled. New versions go to `testing` first and move to `release` after 7 days.


*Available in the next LFOps release.*


## How the Role Behaves

* The role writes the same files as the `linuxfabrik-release` package, under the same names and with the same repository IDs (`linuxfabrik`, `linuxfabrik-testing`), so the two do not define the repository twice. Use either of them on a host, not both: installing the package after the role leaves a `linuxfabrik.repo.rpmnew`, and on Debian and Ubuntu dpkg asks whether to keep the `linuxfabrik.sources` the role deployed, which makes an installation without a terminal fail unless apt runs with `--option Dpkg::Options::=--force-confold`. With `lfops__remove_rpmnew_rpmsave`, the role removes the `.rpmnew` and `.dpkg-dist` files on its next run.
* The signing key ships with the role, so the target does not fetch it from the Internet. It is deployed to `/etc/pki/rpm-gpg/RPM-GPG-KEY-linuxfabrik` on the Red Hat family and SUSE, and to `/usr/share/keyrings/linuxfabrik.gpg` on Debian and Ubuntu, where the package keeps it as well.
* dnf and zypper check the signature of the packages, apt checks the signature of the repository metadata. On the Red Hat family and SUSE, the role imports the key into the RPM database, so dnf and zypper do not ask to import it.
* On the Red Hat family, some packages from the repository, for example Glances, depend on EPEL and the CRB repository, which this role does not enable (roles: [linuxfabrik.lfops.repo_epel](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_epel), [linuxfabrik.lfops.repo_baseos](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_baseos)).
* With a mirror URL, the role expects the repository below `<mirror URL>/linuxfabrik/`, in the same layout as on repo.linuxfabrik.ch, for example `<mirror URL>/linuxfabrik/el/9/x86_64/linuxfabrik/release/` or `<mirror URL>/linuxfabrik/debian/linuxfabrik`.
* If the repository cannot be reached, for example because a mirror does not serve it, dnf skips it with an error message (`skip_if_unavailable=1`, as in the package), zypper fails, and on Debian and Ubuntu the run of the role fails at `apt update`.


## Known Limitations

* Supports Debian 11, 12 and 13, Fedora 44, RHEL 8, 9 and 10 and their derivatives, SLES, SLED and openSUSE Leap 15 and 16, and Ubuntu 22.04, 24.04 and 26.04, each on `x86_64` and `aarch64`. The role aborts on other platforms.
* HTTP basic auth for a mirror is supported on the Red Hat family and SUSE only.


## Tags

`repo_linuxfabrik`

* Deploys the Linuxfabrik repository and its signing key.
* Triggers: none.


## Optional Role Variables

`repo_linuxfabrik__basic_auth_login`

* Use HTTP basic auth to login to the repository. Only takes effect together with a custom mirror URL; repo.linuxfabrik.ch does not use basic auth. Defaults to `lfops__repo_basic_auth_login`, making it easy to set this for all `repo_*` roles.
* Type: String.
* Default: `'{{ lfops__repo_basic_auth_login | default("") }}'`

`repo_linuxfabrik__mirror_url`

* Set the URL to a custom mirror server providing the repository. Defaults to `lfops__repo_mirror_url` to allow easily setting the same URL for all `repo_*` roles. If `lfops__repo_mirror_url` is not set, repo.linuxfabrik.ch is used.
* Type: String.
* Default: `'{{ lfops__repo_mirror_url | default("") }}'`

`repo_linuxfabrik__testing_repo_enabled`

* Enables the `testing` channel in addition to the `release` channel. The package manager then installs the newest version from either channel, so new versions arrive 7 days earlier.
* Type: Bool.
* Default: `false`

Example:
```yaml
# optional
repo_linuxfabrik__basic_auth_login:
  username: 'my-username'
  password: 'linuxfabrik'
repo_linuxfabrik__mirror_url: 'https://mirror.example.com'
repo_linuxfabrik__testing_repo_enabled: true
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
