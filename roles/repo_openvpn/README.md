# Ansible Role linuxfabrik.lfops.repo_openvpn

This role deploys the [OpenVPN 2.7 release repository](https://copr.fedorainfracloud.org/coprs/g/OpenVPN/openvpn-release-2.7/), which the OpenVPN community maintains on Fedora Copr.


*Available in the next LFOps release.*


## How the Role Behaves

* The repository is the place to get OpenVPN 2.7 on RHEL 8 and 9: EPEL ships OpenVPN 2.4 on RHEL 8 and 2.5 on RHEL 9, both end-of-life upstream. On RHEL 10, EPEL ships a 2.7 release as well, but it lags behind the Copr repository.
* The repository file has the same name and repository ID as the one `dnf copr enable @OpenVPN/openvpn-release-2.7` creates, so a repository enabled by hand before is taken over instead of being defined twice.
* The repository signing key ships with the role and is deployed to `/etc/pki/rpm-gpg/`, so the target does not fetch it from the Internet.
* With a mirror URL, the role expects the packages below `<mirror URL>/copr/OpenVPN/openvpn-release-2.7/epel-<RHEL major version>-x86_64/`.
* The OpenVPN packages in this repository recommend `kmod-ovpn`, which pulls DKMS, a compiler and the kernel headers onto the host. Install `openvpn` without weak dependencies, as the [openvpn_server](https://github.com/Linuxfabrik/lfops/tree/main/roles/openvpn_server) role does.


## Dependent Roles

Any [LFOps playbook](https://github.com/Linuxfabrik/lfops/blob/main/playbooks/README.md) that installs this role runs these for you. Optional ones can be disabled via the playbook's skip variables.

* The EPEL repository must be enabled (role: [linuxfabrik.lfops.repo_epel](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_epel)). OpenVPN from this repository needs `pkcs11-helper` from EPEL on RHEL 8 and 10.


## Known Limitations

* Supports RHEL 8, 9 and 10 and their derivatives only. The role aborts on other platforms.


## Tags

`repo_openvpn`

* Deploys the OpenVPN repository and its signing key.
* Triggers: none.


## Optional Role Variables

`repo_openvpn__basic_auth_login`

* Use HTTP basic auth to login to the repository. Only takes effect together with a custom mirror URL; the upstream repository does not use basic auth. Defaults to `lfops__repo_basic_auth_login`, making it easy to set this for all `repo_*` roles.
* Type: String.
* Default: `'{{ lfops__repo_basic_auth_login | default("") }}'`

`repo_openvpn__mirror_url`

* Set the URL to a custom mirror server providing the repository. Defaults to `lfops__repo_mirror_url` to allow easily setting the same URL for all `repo_*` roles. If `lfops__repo_mirror_url` is not set, the upstream repository is used.
* Type: String.
* Default: `'{{ lfops__repo_mirror_url | default("") }}'`

Example:
```yaml
# optional
repo_openvpn__basic_auth_login:
  username: 'my-username'
  password: 'linuxfabrik'
repo_openvpn__mirror_url: 'https://mirror.example.com'
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
