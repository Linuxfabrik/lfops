# Ansible Role linuxfabrik.lfops.numishare

This role checks out [Numishare](https://github.com/ewg118/numishare) — an open-source platform for managing and publishing numismatic collections — and wires it up against an existing eXist-db (XML database), Apache Solr (search backend) and Apache Tomcat / Orbeon Forms (web layer).

The role:

* Installs `git-core` and shallow-clones the Numishare repository into `numishare__install_dir` (default `/opt/numishare`).
* Deploys `exist-config.xml` so Numishare knows how to reach eXist-db.
* Deploys `solr-home/<core_version>/core.properties` so Solr can pick up the Numishare core, and creates the `<solr_data_dir>/<core_name>` symlink Solr's `solr.solr.home` scanner expects. Notifies a Solr restart so the core is loaded.
* Creates `numishare__themes_dir` (default `/opt/themes`) and exposes Numishare's bundled UI assets as the `default` theme via a symlink.
* Deploys custom themes from git or tarball sources via the `numishare__themes__*` variable family.
* Deploys per-collection Numishare projects (the XPL pipelines / views the public `/numishare/<collection>/` pages render through) from git or tarball sources via the `numishare__projects__*` variable family, into `numishare__projects_dir`, and rewrites each project's own `exist-config.xml` to `numishare__exist_url` (project pipelines read it via the project-relative `../../exist-config.xml`, so the upstream `localhost:8080` default would otherwise make every collection page 404). The `orbeon_forms` role wires this into the Orbeon `oxf:/numishare-projects/` resource path.

Numishare itself is end-of-life upstream but stable; this role pins to the upstream `main` branch (one-time clone, updates handled out-of-band) and adapts the surrounding integration layer instead.

This role is intended to be used together with [linuxfabrik.lfops.existdb](https://github.com/Linuxfabrik/lfops/tree/main/roles/existdb), [linuxfabrik.lfops.apache_solr](https://github.com/Linuxfabrik/lfops/tree/main/roles/apache_solr), [linuxfabrik.lfops.apache_tomcat](https://github.com/Linuxfabrik/lfops/tree/main/roles/apache_tomcat), and [linuxfabrik.lfops.orbeon_forms](https://github.com/Linuxfabrik/lfops/tree/main/roles/orbeon_forms). The [setup_numishare](https://github.com/Linuxfabrik/lfops/blob/main/playbooks/setup_numishare.yml) playbook wires them all up in the right order.


*Available in the next LFOps release.*


## Dependent Roles

Any [LFOps playbook](https://github.com/Linuxfabrik/lfops/blob/main/playbooks/README.md) that installs this role runs these for you. Optional ones can be disabled via the playbook's skip variables.

* Apache Solr must be running with `solr.solr.home` set to `numishare__solr_data_dir` (role: [linuxfabrik.lfops.apache_solr](https://github.com/Linuxfabrik/lfops/tree/main/roles/apache_solr)).
* eXist-db must be running and reachable at `numishare__exist_url` (role: [linuxfabrik.lfops.existdb](https://github.com/Linuxfabrik/lfops/tree/main/roles/existdb)).
* Apache Tomcat must be installed — it creates the `tomcat` user that owns Numishare's config files (role: [linuxfabrik.lfops.apache_tomcat](https://github.com/Linuxfabrik/lfops/tree/main/roles/apache_tomcat)).


## Tags

`numishare`

* Installs `git-core`, clones Numishare, deploys `exist-config.xml`, wires the Solr core, creates `/opt/themes/` plus the `default` theme symlink, and deploys all custom themes listed in `numishare__themes__*`.
* Triggers: solr.service restart on Solr-core changes.


## Mandatory Role Variables

None. All variables have defaults; the eXist-db admin password defaults to `'linuxfabrik'` and **must** be overridden via `numishare__exist_password` (or by setting `existdb__admin_password` and inheriting it) for any non-throwaway install.


## Optional Role Variables

`numishare__app_group`

* Group that owns Numishare config files (must match the application server user).
* Type: String.
* Default: `'tomcat'`

`numishare__app_user`

* User that owns Numishare config files (must match the application server user).
* Type: String.
* Default: `'tomcat'`

`numishare__exist_password`

* Password used by Numishare to authenticate against eXist-db.
* Type: String.
* Default: `'linuxfabrik'` — change this.

`numishare__exist_url`

* eXist-db REST endpoint Numishare connects to. `127.0.0.1` is preferred over `localhost` because eXist-db's Jetty binds IPv4 only.
* Type: String.
* Default: `'http://127.0.0.1:8888/exist/rest/db/'`

`numishare__exist_username`

* User Numishare authenticates as against eXist-db. Typically the eXist-db `admin`.
* Type: String.
* Default: `'admin'`

`numishare__git_url`

* Upstream Numishare repository to clone.
* Type: String.
* Default: `'https://github.com/ewg118/numishare.git'`

`numishare__install_dir`

* Where Numishare is checked out to.
* Type: String.
* Default: `'/opt/numishare'`

`numishare__projects_dir`

* Root directory for Numishare projects. Each direct subdirectory is one project, resolved by Numishare's page-flow via `oxf:/numishare-projects/<name>/...`. The `orbeon_forms` role symlinks the Orbeon resource path `WEB-INF/resources/numishare-projects` to this directory.
* Type: String.
* Default: `'/opt/numishare-projects'`

`numishare__projects__host_var` / `numishare__projects__group_var`

* List of per-collection Numishare projects to deploy under `numishare__projects_dir`. A project is the upstream Numishare per-collection deployment (XPL pipelines, views, XSLT) that the public `/numishare/<collection>/` pages render through; distinct from a theme, which carries only static UI assets. Each entry is one of two source types: `git_url` (clones the repo) or `tarball_url` (downloads + extracts).
* Type: List of dictionaries.
* Default: `[]`
* Subkeys:

    * `name`:

        * Mandatory. Project directory name under `numishare__projects_dir`. Must match the collection name used in the URL (`/numishare/<name>/`).
        * Type: String.

    * `state`:

        * Optional. Either `present` or `absent`. `absent` removes `<projects_dir>/<name>`.
        * Type: String.
        * Default: `'present'`

    * `git_url`:

        * Mandatory if the project is git-sourced. Mutually exclusive with `tarball_url`.
        * Type: String.

    * `git_version`:

        * Optional. Branch, tag, or commit to check out.
        * Type: String.
        * Default: HEAD of the cloned default branch

    * `git_update`:

        * Optional. Whether subsequent runs should `git pull`.
        * Type: Bool.
        * Default: `false`

    * `tarball_url`:

        * Mandatory if the project is tarball-sourced. Mutually exclusive with `git_url`. `tar.gz`, `tgz`, `tar.bz2` and `zip` are auto-detected. ZIP requires `unzip` on the target.
        * Type: String.

    * `tarball_strip_components`:

        * Optional. `--strip-components=N` for the unarchive step. Use `0` for tarballs without a wrapping top-level directory.
        * Type: Number.
        * Default: `1`

Example:

```yaml
numishare__projects__host_var:
  - name: 'oscar'
    git_url: 'https://github.com/ewg118/numishare.git'
    git_version: 'oscar'
    git_update: false
    state: 'present'
```

`numishare__solr_core_name`

* Name of the Solr core Numishare uses.
* Type: String.
* Default: `'numishare'`

`numishare__solr_core_version`

* Numishare's Solr schema version. Determines which `solr-home/<version>/` sub-directory is wired up.
* Type: String.
* Default: `'1.7'`

`numishare__solr_data_dir`

* Solr's `solr.solr.home`. The role creates `<solr_data_dir>/<solr_core_name>` as a symlink to `<install_dir>/solr-home/<solr_core_version>/`.
* Type: String.
* Default: `'/var/solr/data'`

`numishare__solr_group`

* Group that owns the Solr-related Numishare files.
* Type: String.
* Default: `'solr'`

`numishare__solr_user`

* User that owns the Solr-related Numishare files.
* Type: String.
* Default: `'solr'`

`numishare__themes_dir`

* Root directory for custom Numishare themes. Each direct subdirectory is a theme. The role auto-creates `<themes_dir>/default` as a symlink to Numishare's bundled UI assets.
* Type: String.
* Default: `'/opt/themes'`

`numishare__themes__host_var` / `numishare__themes__group_var`

* List of themes to deploy under `numishare__themes_dir`. Each entry is one of two source types: `git_url` (clones the repo) or `tarball_url` (downloads + extracts).
* Type: List of dictionaries.
* Default: `[]`
* Subkeys:

    * `name`:

        * Mandatory. Theme directory name under `numishare__themes_dir`.
        * Type: String.

    * `state`:

        * Optional. Either `present` or `absent`. `absent` removes `<themes_dir>/<name>`.
        * Type: String.
        * Default: `'present'`

    * `git_url`:

        * Mandatory if the theme is git-sourced. Mutually exclusive with `tarball_url`.
        * Type: String.

    * `git_version`:

        * Optional. Branch, tag, or commit to check out.
        * Type: String.
        * Default: HEAD of the cloned default branch

    * `git_update`:

        * Optional. Whether subsequent runs should `git pull`.
        * Type: Bool.
        * Default: `false`

    * `tarball_url`:

        * Mandatory if the theme is tarball-sourced. Mutually exclusive with `git_url`. `tar.gz`, `tgz`, `tar.bz2` and `zip` are auto-detected. ZIP requires `unzip` on the target.
        * Type: String.

    * `tarball_strip_components`:

        * Optional. `--strip-components=N` for the unarchive step. Use `0` for tarballs without a wrapping top-level directory.
        * Type: Number.
        * Default: `1`

Example:

```yaml
numishare__themes__host_var:
  - name: 'example'
    git_url: 'https://git.example.com/themes/numishare-theme-example.git'
    git_version: 'main'
    state: 'present'
  - name: 'example-tarball'
    tarball_url: 'https://artifacts.example.com/numishare-theme-example-tarball-1.2.0.tar.gz'
    state: 'present'
  - name: 'example-old'
    state: 'absent'
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
