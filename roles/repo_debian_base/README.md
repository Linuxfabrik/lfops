# Ansible Role linuxfabrik.lfops.repo_debian_base

This role deploys `/etc/apt/sources.list` for Debian, allowing you to point the host at a custom mirror server. It is Debian-only; running it against an Ubuntu or Red Hat-family host fails because there is no matching template.

Supported Debian versions: 10, 11, 12. The version is auto-detected via `ansible_facts["distribution_major_version"]` and the matching template is rendered.

After deploying the sources list, the role removes any `.rpmnew` / `.dpkg-dist` / `.ucf-dist` siblings if `lfops__remove_rpmnew_rpmsave: true` is set globally. By default these files are kept.


## Tags

`repo_debian_base`

* Deploys `/etc/apt/sources.list`.
* Triggers: none.


## Optional Role Variables

`repo_debian_base__mirror_url`

* Set the URL to a custom mirror server providing the repository. Defaults to `lfops__repo_mirror_url` to allow easily setting the same URL for all `repo_*` roles. If `lfops__repo_mirror_url` is not set either, the default Debian mirrors are used.
* Type: String.
* Default: `'{{ lfops__repo_mirror_url | default("") }}'`

Example:
```yaml
# optional
repo_debian_base__mirror_url: 'https://mirror.example.com'
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
