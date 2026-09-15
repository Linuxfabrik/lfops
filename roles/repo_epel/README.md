# Ansible Role linuxfabrik.lfops.repo_epel

This role deploys the [Extra Packages for Enterprise Linux (EPEL) Repository](https://docs.fedoraproject.org/en-US/epel/).


*Available since LFOps `1.0.0`.*


## Dependent Roles

Any [LFOps playbook](https://github.com/Linuxfabrik/lfops/blob/main/playbooks/README.md) that installs this role runs these for you. Optional ones can be disabled via the playbook's skip variables.

* On Rocky 9 and newer, the CRB repository must be enabled, because EPEL packages depend on packages from it (role: [linuxfabrik.lfops.repo_baseos](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_baseos)). On Rocky, AlmaLinux and CentOS 8, this role enables the equivalent PowerTools repository itself.


## Tags

`repo_epel`

* Deploys the EPEL Repository.
* Triggers: none.


## Optional Role Variables

`repo_epel__basic_auth_login`

* Use HTTP basic auth to login to the repository. Only takes effect together with a custom mirror URL; the default public repositories do not use basic auth. Defaults to `lfops__repo_basic_auth_login`, making it easy to set this for all `repo_*` roles.
* Type: String.
* Default: `'{{ lfops__repo_basic_auth_login | default("") }}'`

`repo_epel__epel_cisco_openh264_enabled`

* Whether the "epel-cisco-openh264" repository should be enabled or not.
* Type: Bool.
* Default: `true`

`repo_epel__mirror_url`

* Set the URL to a custom mirror server providing the repository. Defaults to `lfops__repo_mirror_url` to allow easily setting the same URL for all `repo_*` roles. If `lfops__repo_mirror_url` is not set, the default mirrors of the repo are used.
* Type: String.
* Default: `'{{ lfops__repo_mirror_url | default("") }}'`

Example:
```yaml
# optional
repo_epel__basic_auth_login:
  username: 'my-username'
  password: 'linuxfabrik'
repo_epel__epel_cisco_openh264_enabled: true
repo_epel__mirror_url: 'https://mirror.example.com'
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
