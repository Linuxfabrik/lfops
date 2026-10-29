# Ansible Role linuxfabrik.lfops.repo_opensearch

This role deploys the [OpenSearch Package Repository](https://docs.opensearch.org/latest/install-and-configure/install-opensearch/rpm/) for OpenSearch 2.x or 3.x.


*Available since LFOps `2.0.0`.*


## Known Limitations

* OpenSearch 2.x cannot be installed on RHEL 10 and Debian 13. The OpenSearch 2.x signing key (`opensearch.pgp`) binds its user ID with a SHA-1 signature, which the default crypto policy of these releases rejects. On RHEL 10, `dnf` fails with `Policy rejects 39D319879310D3FC: No binding signature at time ...` and `Error: GPG check FAILED`. On Debian 13, `apt update` fails with `SHA1 is not considered secure since 2026-02-01T00:00:00Z` and `The repository ... is not signed`. Use OpenSearch 3.x there, whose key (`opensearch-release.pgp`) is not affected. This role does not weaken the crypto policy.
* On RHEL 9, `dnf` imports the OpenSearch 2.x key and installs the packages, but a manual `rpmkeys --import` of the same key fails with `Hash algorithm SHA1 not available`.


## Tags

`repo_opensearch`

* Deploys the OpenSearch Package Repository.
* Triggers: none.


## Mandatory Role Variables

`repo_opensearch__version__host_var` / `repo_opensearch__version__group_var`

* The version of the OpenSearch repository which should be installed. One of `'2.x'` or `'3.x'`. For the usage in `host_vars` / `group_vars` (can only be used in one group at a time).
* Type: String.

Example:
```yaml
# mandatory
repo_opensearch__version__host_var: '2.x'
```


## Optional Role Variables

`repo_opensearch__basic_auth_login`

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

`repo_opensearch__mirror_url`

* Set the URL to a custom mirror server providing the repository. Defaults to `lfops__repo_mirror_url` to allow easily setting the same URL for all `repo_*` roles. If `lfops__repo_mirror_url` is not set, the default mirrors of the repo are used.
* Type: String.
* Default: `'{{ lfops__repo_mirror_url | default("") }}'`

Example:
```yaml
# optional
repo_opensearch__basic_auth_login:
  username: 'my-username'
  password: 'linuxfabrik'
repo_opensearch__mirror_url: 'https://mirror.example.com'
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
