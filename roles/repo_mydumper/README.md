# Ansible Role linuxfabrik.lfops.repo_mydumper

This role deploys a repository for the mydumper package.
By default, it uses the official [APT and YUM repositories](https://mydumper.github.io/mydumper/docs/html/installing.html) of the mydumper project, and verifies the packages against the project's GPG key.


*Available since LFOps `2.0.0`.*


## Tags

`repo_mydumper`

* Deploys the mydumper repository.
* Triggers: none.


## Optional Role Variables

`repo_mydumper__basic_auth_login`

* Use HTTP basic auth to login to the repository. Only takes effect together with a custom mirror URL; the default public repositories do not use basic auth. Defaults to `lfops__repo_basic_auth_login`, making it easy to set this for all `repo_*` roles.
* Type: Dictionary.
* Default: `'{{ lfops__repo_basic_auth_login | default("") }}'`
* Subkeys:

    * `password`:

        * Mandatory. Password.
        * Type: String.

    * `username`:

        * Mandatory. Username.
        * Type: String.

`repo_mydumper__mirror_url`

* Set the URL to a custom mirror server providing the repository. Defaults to `lfops__repo_mirror_url` to allow easily setting the same URL for all `repo_*` roles. If `lfops__repo_mirror_url` is not set, the default mirrors of the repo are used.
* Type: String.
* Default: `'{{ lfops__repo_mirror_url | default("") }}'`

Example:
```yaml
# optional
repo_mydumper__basic_auth_login:
  username: 'my-username'
  password: 'linuxfabrik'
repo_mydumper__mirror_url: 'https://mirror.example.com'
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
