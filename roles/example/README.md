# Ansible Role linuxfabrik.lfops.example

This role installs and configures [Example](https://example.com/). Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.

This role also serves as a reference for consistent role development across LFOps. All `ansible.builtin.*` modules used in `tasks/main.yml` are documented with their most common parameters. The section structure below is the canonical menu for every role README: keep the sections in this order, drop the optional ones that do not apply, and never invent new top-level sections.

This role is compatible with the following example versions:

* 1.0.0
* 2.0.0


<!--
"Available since" marks the LFOps release in which the role first shipped. Set it once and
never change it afterwards. When you add a new role you do not know the next version tag yet,
so write the literal line `*Available in the next LFOps release.*` instead; it is rewritten to
the real version with sed when the next release is prepared. Place it after the version-compat block
(or after the intro when there is none), with two blank lines above and below (the same spacing
that separates every section in this template).
-->
*Available since LFOps `2.0.0`.*


<!--
optional. Proactive, non-obvious design/runtime notes the engineer must understand before
running the role: controller-vs-target download split and who needs network access,
idempotency / overwrite-on-rerun, the upgrade path, hard-coded versions, OS-specific build
dependencies, what the role does NOT do, and security caveats (e.g. cleartext secrets).
Distinct from Troubleshooting (reactive error->fix) and Known Limitations (hard constraints).
-->
## How the Role Behaves

* The release tarball is downloaded on the Ansible controller (`delegate_to: 'localhost'`) and copied to the target, so targets without Internet access can still be provisioned. The controller needs outbound access to `example.com`; the target does not.
* Configuration is fully templated. On every run the files under `/etc/example/` are re-rendered from the role's templates (a timestamped backup is kept), so out-of-band manual edits are overwritten. Manage all settings through the role variables below.
* A configuration change notifies a chained handler that first runs `example --validate-config` and then restarts `example.service`. The restart is skipped when the service was just started in the same run or when `example__service_state` is `stopped`.
* Version-specific defaults are loaded from the *installed* package version (`vars/<version>.yml`), not from `example__version`.
* On Red Hat-family hosts the role manages the SELinux port type and the `httpd_can_network_connect` boolean, but only when SELinux is not disabled.
* This role does not manage the firewall or TLS certificates. Open the listener ports and provide certificates separately.


<!-- optional. Terse bullet list of hard constraints the operator cannot work around (version gaps, unsupported topologies). -->
## Known Limitations

* The role configures a single standalone node; clustering is not supported.
* Downgrades are not tested. Lowering `example__version` after installation may leave stale files under `/opt/example`.


<!--
optional. The other LFOps roles this role depends on. Any LFOps playbook that installs this
role (its `X.yml`, or a bundling `setup_X.yml`) wires these in for you. Two groups:
  * Roles the playbook runs by default go in the first list, right under the lead-in. A plain
    bullet is mandatory; an "Optional:" bullet is feature-optional (the playbook still runs it,
    but it can be skipped).
  * Roles the playbook ships but leaves OFF by default go under a "These roles are not enabled
    by default; enable them via the playbook's skip variables if needed:" list-title. Omit this
    list when there are none.
Write each bullet declaratively (a state: "must be enabled"), name the role, and give the "why"
when it is not obvious. Do NOT list skip-variable names or the exact play order - those live
solely in playbooks/README.md. A dependency that needs a SEPARATE playbook (a database server,
a central server, ...) is not a dependent role of this playbook; put it under "## Requirements".
-->
## Dependent Roles

Any [LFOps playbook](https://github.com/Linuxfabrik/lfops/blob/main/playbooks/README.md) that installs this role runs these for you. Optional ones can be disabled via the playbook's skip variables.

* The example repository must be enabled (role: [linuxfabrik.lfops.repo_example](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_example)). The example packages are served from it.
* Optional: the optional dependency (role: [linuxfabrik.lfops.optional_dependency](https://github.com/Linuxfabrik/lfops/tree/main/roles/optional_dependency)) enables the optional feature.

These roles are not enabled by default; enable them via the playbook's skip variables if needed:

* An alternative cache backend (role: [linuxfabrik.lfops.example_cache](https://github.com/Linuxfabrik/lfops/tree/main/roles/example_cache)) replaces the built-in cache.


<!--
optional. Everything the operator must provide that this role's playbook does NOT do for you.
Two kinds, in this order:
  * provided-state prerequisites as plain bullets: host resources, an external account or
    subscription, credentials you supply.
  * hands-on procedures under a "Manual steps:" list-title, written imperatively: run a SEPARATE
    playbook for a dependency, mint a token in a web console, install something on the Ansible
    controller, configure DNS.
Mark feature-optional items with "Optional:".
-->
## Requirements

* At least 2 GB RAM on the target host.
* Outbound HTTPS access from the target to `example.com` for license validation.

Manual steps:

* Deploy a database server first by running the  [linuxfabrik.lfops.mariadb_server](https://github.com/Linuxfabrik/lfops/tree/main/roles/mariadb_server) role. The example role expects an existing database.
* Obtain an API token from the Example web console and store it in your inventory as `example__api_token`.
* Optional: install the Example CLI on the Ansible controller (`pip install example-cli`) to use the `example:inspect` helper tasks.


<!--
optional operational walkthrough. Only for roles that need a procedural guide (clustering,
multi-instance setups). Keep it in this position (after Requirements, before
Post-Installation Steps). Prefer one of these titles, but a descriptive role-specific title is
allowed when none fits:
  ## Single-Node Setup
  ## Cluster Setup
  ## Adding a Node to an Existing Cluster
  ## <descriptive title>   (e.g. bind "Primary-Secondary Example")
Procedural sub-steps inside a walkthrough may use `###` subheadings.
The example role is a single standalone service, so it has no walkthrough.
-->


<!-- optional. Manual steps the operator must perform AFTER the role completes (e.g. reset a generated password, finish a setup wizard, verify the cluster is healthy). -->
## Post-Installation Steps

* Retrieve the initial admin password from `/var/lib/example/initial-admin-password` and change it on first login.


## Tags

`example`

* Installs required packages and plugins.
* Creates the example system user and group.
* Deploys the configuration files.
* Ensures the example service is in the desired state.
* Triggers: example.service restart.

`example:configure`

* Deploys configuration files.
* Triggers: example.service restart.

`example:state`

* Manages the service state (start, stop, enable, disable).
* Triggers: none.

`example:plugin`

* Manages optional example plugins (install/remove).
* Triggers: none.

`example:user`

* Manages application users via the REST API.
* Triggers: none.


## Mandatory Role Variables

`example__version`

* The version of example to install.
* Type: String.

Example:
```yaml
# mandatory
example__version: '3.2.1'
```


<!-- optional. Variables that are technically optional but strongly advised in practice; omitting them leaves an important feature off. -->
## Recommended Role Variables

`example__backup_target`

* Where nightly dumps are written. Strongly recommended in production; without it no backups are taken.
* Type: String.
* Default: `''` (no backups)


## Optional Role Variables

`example__conf_log_level__host_var` / `example__conf_log_level__group_var`

* The log level.
* Type: String. One of `debug`, `info`, `warn`, `error`.
* Default: `'info'`

`example__conf_max_connections__host_var` / `example__conf_max_connections__group_var`

* Maximum number of concurrent connections. Must be between 1 and 10000.
* Type: Number.
* Default: `100`

`example__conf_worker_threads`

* Number of worker threads for request processing.
* Type: Number.
* Default: 1.0.0: `4`, 2.0.0: `8`

`example__lib_version`

* The version of the [Linuxfabrik Python Libraries](https://github.com/Linuxfabrik/lib) to install.
* Type: String.

`example__listeners__host_var` / `example__listeners__group_var`

* Network listeners for the example service. Items are identified by a composite key of `name` + `port`, allowing the same name on different ports.
* Type: List of dictionaries.
* Default:

    ```yaml
    - name: 'default'
      port: 8080
    - name: 'default'
      port: 8443
      ssl: true
    ```

* Subkeys:

    * `name`:

        * Mandatory. Listener name.
        * Type: String.

    * `port`:

        * Mandatory. Port number.
        * Type: Number.

    * `ssl`:

        * Optional. Enable SSL for this listener.
        * Type: Bool.
        * Default: `false`

    * `state`:

        * Optional. `present` or `absent`.
        * Type: String.
        * Default: `'present'`

`example__logrotate`

* Log files are rotated `count` days before being removed. If count is `0`, old versions are removed rather than rotated. If count is `-1`, old logs are not removed at all (use with caution, may waste performance and disk space).
* Type: Number.
* Default: `{{ logrotate__rotate | d(14) }}`

`example__maintenance_cron_minute`

* Minute of the hour at which the maintenance cron job runs.
* Type: Number.
* Default: `{{ 59 | random(seed=inventory_hostname) }}`

`example__plugins__host_var` / `example__plugins__group_var`

* Optional plugins to install as OS packages.
* Type: List of dictionaries.
* Default: `[]`
* Subkeys:

    * `name`:

        * Mandatory. Package name of the plugin.
        * Type: String.

    * `state`:

        * Optional. `present` or `absent`.
        * Type: String.
        * Default: `'present'`

`example__service_enabled`

* Enables or disables the service, analogous to `systemctl enable/disable --now`.
* Type: Bool.
* Default: `true`

`example__service_state`

* Changes the state of the service, analogous to `systemctl start/stop/restart/reload`.
* Type: String. One of `reloaded`, `restarted`, `started`, `stopped`.
* Default: `'started'`

`example__users__host_var` / `example__users__group_var`

* Application users to manage.
* Type: List of dictionaries.
* Default: `[]`
* Subkeys:

    * `name`:

        * Mandatory. Username.
        * Type: String.

    * `password`:

        * Mandatory for `state: 'present'` users. Password.
        * Type: String.

    * `comment`:

        * Optional. User description.
        * Type: String.

    * `state`:

        * Optional. `present` or `absent`.
        * Type: String.
        * Default: `'present'`

Example:
```yaml
# optional
example__conf_log_level__host_var: 'debug'
example__conf_max_connections__host_var: 200
example__conf_worker_threads: 16
example__lib_version: '2.4.0'
example__listeners__host_var:
  - name: 'default'
    port: 8443
    state: 'absent'
  - name: 'api'
    port: 9090
example__logrotate: 7
example__maintenance_cron_minute: 30
example__plugins__host_var:
  - name: 'example-plugin-auth-ldap'
  - name: 'example-plugin-cache-redis'
  - name: 'example-plugin-legacy-api'
    state: 'absent'
example__service_enabled: true
example__service_state: 'started'
example__users__host_var:
  - name: 'example-admin'
    password: 'linuxfabrik'
    comment: 'Admin Account'
  - name: 'old-user'
    state: 'absent'
```


<!--
optional, repeatable. Large roles MAY split the variables into subgroups. Use the upstream
module name (`- mod_ssl`), the variable prefix as a code span
(`` - `example__conf_tls_*` Config Directives ``), or a functional label (`- vHosts`). These
suffixed sections are the same canonical section repeated; give each its own Example block.
The same applies to `## Mandatory Role Variables - <Subgroup>`, and a subgroup MAY keep its
own Mandatory and Optional sections paired together (group-by-module) instead of forcing all
mandatory subgroups before all optional ones. A variable grouping must always be its own `##`
section; do not demote it to a `###` subheading inside `## Optional Role Variables`.
-->
## Optional Role Variables - `example__conf_tls_*` Config Directives

`example__conf_tls_protocols`

* Allowed TLS protocol versions.
* Type: String.
* Default: `'TLSv1.2 TLSv1.3'`

Example:
```yaml
# optional
example__conf_tls_protocols: 'TLSv1.3'
```


<!-- optional. Reactive Q&A: concrete error messages or symptoms and how to fix them. -->
## Troubleshooting

**`example.service` fails to start with `bind: address already in use`**

* Another process occupies a configured port. Change the affected `example__listeners` entry or stop the conflicting service.


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
