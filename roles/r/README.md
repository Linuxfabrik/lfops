# Ansible Role linuxfabrik.lfops.r

This role installs [R](https://www.r-project.org/) together with pandoc, points R at a binary CRAN mirror, and installs the CRAN packages an application needs.

EPEL ships R itself but next to no CRAN packages: around two dozen `R-*` packages per RHEL generation, among which `R-shiny`, `R-rmarkdown`, `R-dplyr` and `R-data.table` are not. Everything beyond the base therefore comes through `install.packages()`, which this role drives.


*Available in the next LFOps release.*


## How the Role Behaves

* CRAN itself serves source only, so every package with a C or C++ part is compiled locally, which costs minutes for `data.table`, `dplyr` or `ggplot2`. The role configures the [Posit Public Package Manager](https://packagemanager.posit.co/) instead, which serves prebuilt binaries for the RHEL family. The path component differs per generation and is selected automatically (RHEL 8 uses `centos8`, there is no `rhel8` path).
* The package manager decides from the HTTP user agent whether it hands out a binary or a source package. Without `HTTPUserAgent`, R silently compiles from source despite the binary repository, so the role writes both settings together. Check with `R --quiet -e 'cat(getOption("HTTPUserAgent"))'`.
* `Rprofile.site` and `Renviron.site` are not shipped by the R packages. The role creates both and re-renders them on every run, so manual edits are overwritten; a timestamped backup is kept.
* `latest` in the repository URL always resolves to the current CRAN state, so two installations on different days produce different package versions. Where that matters, set `r__cran_repo_url` to a dated snapshot URL, or manage an application's dependencies with [renv](https://rstudio.github.io/renv/) and keep its `renv.lock` next to the application code.
* A CRAN package is installed only when it is absent from the library, and removed only when it is present, so a second run reports no change. The role does not upgrade installed packages.
* `install.packages()` reports a failed installation as a warning and still exits 0, so the role asks the library afterwards whether the package really arrived and fails the run when it did not.
* The role does not manage per-user or per-project libraries. Everything is installed into the system library, which is the first entry of `.libPaths()`.


## Dependent Roles

Any [LFOps playbook](https://github.com/Linuxfabrik/lfops/blob/main/playbooks/README.md) that installs this role runs these for you. Optional ones can be disabled via the playbook's skip variables.

* The EPEL repository must be enabled (role: [linuxfabrik.lfops.repo_epel](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_epel)). R comes from it, and on RHEL 9 and 10 pandoc as well.
* The CRB repository must be enabled on RHEL 9 and 10 (role: [linuxfabrik.lfops.repo_baseos](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_baseos)). It carries the development packages the CRAN packages are built against. On RHEL 8 the same repository is called PowerTools, is enabled by the `repo_epel` role, and additionally provides pandoc itself.


## Requirements

* Outbound HTTPS access from the target host to `packagemanager.posit.co`, or to the mirror configured in `r__cran_repo_url`.


## Tags

`r`

* Installs R, pandoc and the build dependencies.
* Deploys `Rprofile.site` and `Renviron.site`.
* Installs and removes the CRAN packages.
* Triggers: none.

`r:configure`

* Deploys `Rprofile.site` and `Renviron.site`.
* Triggers: none.

`r:modules`

* Installs and removes the CRAN packages.
* Triggers: none.


## Optional Role Variables

`r__cran_packages__host_var` / `r__cran_packages__group_var`

* CRAN packages to install.
* Type: List of dictionaries.
* Default: `[]`
* Subkeys:

    * `name`:

        * Mandatory. Name of the CRAN package.
        * Type: String.

    * `state`:

        * Optional. `present` or `absent`.
        * Type: String.
        * Default: `'present'`

`r__cran_repo_url`

* Repository `install.packages()` reads from.
* Type: String.
* Default: RHEL 8: `'https://packagemanager.posit.co/cran/__linux__/centos8/latest'`, RHEL 9: `'https://packagemanager.posit.co/cran/__linux__/rhel9/latest'`, RHEL 10: `'https://packagemanager.posit.co/cran/__linux__/rhel10/latest'`
* Deviates from the upstream default `https://cloud.r-project.org`: CRAN serves source packages only, so the upstream default turns every installation of a package with compiled code into a local build.

`r__http_user_agent_enabled`

* Set `HTTPUserAgent` so that the Posit Public Package Manager serves binary packages. Turn this off only for a mirror that ignores the user agent.
* Type: Bool.
* Default: `true`

`r__renviron_site__host_var` / `r__renviron_site__group_var`

* Environment variables written to `Renviron.site`. This is the only reliable place for the environment of an R process started by Shiny Server, which goes through `su --login` and therefore never sees the environment of the service.
* Type: List of dictionaries.
* Default: `[]`
* Subkeys:

    * `name`:

        * Mandatory. Name of the environment variable.
        * Type: String.

    * `value`:

        * Mandatory. Value of the environment variable.
        * Type: String.

    * `state`:

        * Optional. `present` or `absent`.
        * Type: String.
        * Default: `'present'`

`r__renviron_site_raw`

* Verbatim content appended to `Renviron.site`.
* Type: String.
* Default: `''`

`r__rprofile_site_raw`

* Verbatim R code appended to `Rprofile.site`.
* Type: String.
* Default: `''`

`r__skip_build_dependency_installation`

* Skip the installation of the development packages of the C libraries CRAN packages link against. They all come from AppStream, and without them a package the Posit Public Package Manager has no binary for cannot be built.
* Type: Bool.
* Default: `false`

Example:
```yaml
# optional
r__cran_packages__host_var:
  - name: 'data.table'
  - name: 'ggplot2'
  - name: 'obsolete-package'
    state: 'absent'
r__cran_repo_url: 'https://packagemanager.posit.co/cran/__linux__/rhel9/2026-06-01'
r__http_user_agent_enabled: true
r__renviron_site__host_var:
  # reticulate embeds a Python interpreter in the R session; the interpreter is best named
  # centrally, because the application code cannot rely on the environment it inherits
  - name: 'RETICULATE_PYTHON'
    value: '/usr/bin/python3'
r__renviron_site_raw: |
  R_LIBS_SITE=/opt/r-site-library
r__rprofile_site_raw: |
  options(warn = 1)
r__skip_build_dependency_installation: false
```


## Troubleshooting

**`install.packages()` compiles from source for hours**

* `HTTPUserAgent` is missing or wrong, so the Posit Public Package Manager serves source packages. Check with `R --quiet -e 'cat(getOption("HTTPUserAgent"))'`. With the setting in place, R reports `* installing *binary* package '...'` and finishes in seconds, and `R --quiet -e "cat(packageDescription('data.table')\$Built)"` shows Posit's build date instead of today's.

**`pandoc version 1.12.3 or higher is required and was not found`**

* The `pandoc` package is missing. Without it, *rmarkdown* renders no reports. Check with `R --quiet -e 'rmarkdown::pandoc_available()'`.

**An application reports `there is no package called '...'`**

* The package is not installed in the system library, or the account running the application cannot read it. Check which library paths that account really sees with `sudo --user=shiny R --quiet -e ".libPaths()"`.


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
