# Ansible Role linuxfabrik.lfops.shiny_server

This role installs and configures [Shiny Server Open Source](https://posit.co/products/open-source/shiny-server/), the Node.js server from Posit that hosts R Shiny applications, and makes it multi-tenant: one Apache httpd vHost per tenant, HTTP basic authentication per tenant, one R worker and one system account per tenant application.

Shiny Server Open Source knows no users, no authentication and no roles. The separation therefore does not happen inside the application but in front of it, in the reverse proxy, and below it, in separate application instances and system accounts.


*Available in the next LFOps release.*


## How the Role Behaves

* Posit publishes one RPM for the whole Red Hat family, built against CentOS 8. It declares no dependencies at all and carries its own Node.js runtime, which is why the same file runs on RHEL 8, 9 and 10. The package is downloaded on the Ansible controller and copied to the target, so targets without Internet access can be provisioned; the controller needs outbound access to `download3.rstudio.org`. It is fetched only when the installed version differs from `shiny_server__version`.
* Updating Shiny Server means raising `shiny_server__version` and running the role again. Posit documents no separate upgrade procedure: the Admin Guide installs the RPM of the wanted version and stops there, which is exactly what the role does, and the package manager resolves it as an upgrade of the installed one. Lowering the version works the same way and downgrades. The package restarts the service as part of its own installation, so an update is a brief outage and takes every running R worker with it. The configuration, the systemd drop-in and the role's logrotate file survive it: the package writes `shiny-server.conf` only when none exists, and it replaces the unit and its own `/etc/logrotate.d/shiny-server` rather than anything below `shiny-server.service.d/`.
* The configuration is deployed **before** the package. The package writes its own `shiny-server.conf` only when none exists, and then enables and starts the service immediately, so without this the service would come up once listening on every interface and serving `/srv/shiny-server` without any access control.
* Shiny Server listens on `127.0.0.1` only. It passes every client header straight through to the R worker, so on a listener reachable from the network a client bypasses the proxy and sets `Shiny-Server-Credentials` itself, which is exactly the value an application reads as `session$user`. The role refuses to run when that header is enabled on a non-loopback listener.
* A configuration change is applied with a reload. The service maps `ExecReload` to `SIGHUP`, on which Shiny Server re-reads its configuration, so no session is dropped. This also means `lfops__skip_restart_handlers` does not defer a configuration change.
* The package overwrites `/etc/systemd/system/shiny-server.service` and `/etc/logrotate.d/shiny-server` on every update. The role therefore never touches either: unit settings go into a drop-in under `/etc/systemd/system/shiny-server.service.d/`, and the rotation of the per-session application logs into a separate `/etc/logrotate.d/shiny-server-apps`. The vendor's own file keeps rotating the daemon log `/var/log/shiny-server.log`.
* Every application gets its own `location`, and therefore its own R worker. This is the reason to give each tenant its own entry even when two tenants run the same code: the default scheduler starts a **single, single-threaded** R worker per application, shared by all its visitors, so two tenants on one instance block each other while one of them computes.
* The role creates the directory structure, the system accounts and the log directories. It does not deploy application code. Put the shared code below `shiny_server__shared_dir` and the per-tenant configuration and data below `shiny_server__tenants_dir`, using symlinks to the shared files rather than copies. Link the individual files, not the whole directory: the working directory of the R process stays the tenant directory that way, so relative paths in the application code find the right tenant's data.
* A tenant account is created with its own primary group and a secondary membership in `shiny_server__shared_group`. The primary group keeps it out of the other tenants' directories, the secondary one lets it read the shared code tree. That shared group is deliberately not the group of the service account: the latter owns the application directory of every location left at the default `run_as`, so using it for both jobs would make those directories readable by all tenants. The account gets no login shell, which does not hinder Shiny Server: it starts the worker as root with `su -s /bin/bash`, which overrides the shell of the account. It does need a home directory, because a worker whose account has none is not started at all.
* An R worker inherits nothing from the service environment. Shiny Server hands it `HOME`, `LANG` and `PATH`, and the `su --login` it goes through then discards those again in favour of the login environment. `TMPDIR`, `R_LIBS`, `RETICULATE_PYTHON` and a full locale therefore belong in `Renviron.site` or `Rprofile.site`, which the `r` role manages.
* Retiring a location with `state: 'absent'` removes what the role created for it: the `location` from the configuration, the application directory **with the tenant's data in it**, the log directory, and the account the application ran as together with its group and home directory. Anything a still-active location shares is kept, so retiring one of a tenant's two applications leaves the account, the log directory and the tenant directory in place. The tenant directory itself goes only once it is empty.
* Deleting a location's entry from the inventory is not the same as retiring it. The entry simply disappears from the merged list, so the location stops being served and nothing on disk is touched. Only an explicit `state: 'absent'` deletes, which is what keeps a mistyped `path` from destroying data.
* The role does not manage TLS. The generated vHosts listen on port 80, for the topology where a reverse proxy in front terminates TLS and the network restricts who may reach this host. Where users connect to this Apache directly, TLS is mandatory, because basic authentication sends the credentials on every request; set `virtualhost_port: 443` per vHost and add the certificate directives through its `raw` key.


## Known Limitations

* Shiny Server Open Source has no authentication, no session management and no per-application resource limits. Basic authentication in front of it cannot log out, expire a session, lock an account after failed attempts or offer a second factor. Where that is needed, Posit Connect or ShinyProxy with one container per user is the answer.
* The separation inside a single application is guaranteed by the application code, not by the platform. All visitors of one application share one R process; everything inside `server <- function(input, output, session)` is per session, everything in `global.R` or above `server()` is shared by all sessions of that application.
* The memory limit in the systemd drop-in protects the host, not the individual session. All sessions of all tenants share the budget, and the OOM killer picks a process inside the control group when it is exceeded.
* Only the x86_64 package is supported. Posit publishes no aarch64 build of Shiny Server.


## Dependent Roles

Any [LFOps playbook](https://github.com/Linuxfabrik/lfops/blob/main/playbooks/README.md) that installs this role runs these for you. Optional ones can be disabled via the playbook's skip variables.

* R and the CRAN packages a Shiny application needs must be installed (role: [linuxfabrik.lfops.r](https://github.com/Linuxfabrik/lfops/tree/main/roles/r)). This role injects `shiny`, `rmarkdown`, `knitr` and `htmltools` into it, plus the `TMPDIR` the uploads land in.
* The reverse proxy in front of the tenants must be configured (role: [linuxfabrik.lfops.apache_httpd](https://github.com/Linuxfabrik/lfops/tree/main/roles/apache_httpd)). This role injects one vHost per tenant, the `.htpasswd` entries, and the `proxy_http` and `proxy_wstunnel` modules that role leaves disabled by default.
* The `python3-passlib` library must be installed (role: [linuxfabrik.lfops.python](https://github.com/Linuxfabrik/lfops/tree/main/roles/python)), because the `.htpasswd` files are written with it.
* On RHEL-compatible systems, the `httpd_can_network_connect` SELinux boolean must be enabled (roles: [linuxfabrik.lfops.policycoreutils](https://github.com/Linuxfabrik/lfops/tree/main/roles/policycoreutils), [linuxfabrik.lfops.selinux](https://github.com/Linuxfabrik/lfops/tree/main/roles/selinux)). Without it Apache cannot reach the Shiny Server port.


## Requirements

* Outbound HTTPS access from the Ansible controller to `download3.rstudio.org`.

Manual steps:

* Look up the current version on the [GitHub Tags page](https://github.com/rstudio/shiny-server/tags) and pin it in `shiny_server__version`.
* Deploy the application code below `shiny_server__shared_dir` and the per-tenant files below `shiny_server__tenants_dir` yourself, from Git or with the [files](https://github.com/Linuxfabrik/lfops/tree/main/roles/files) role.
* Optional: where users reach this Apache directly rather than through a proxy in front, obtain a certificate per tenant hostname (role: [linuxfabrik.lfops.acme_sh](https://github.com/Linuxfabrik/lfops/tree/main/roles/acme_sh)) and add the TLS directives to the vHost through its `raw` key.


## Multi-Tenant Setup

Two tenants with two applications each need two vHosts, not four: the applications become `location` blocks inside the tenant's vHost, and one password per tenant covers all of them.

### 1. Declare one Shiny Server location per tenant application

Each entry becomes a `location` in `shiny-server.conf` and gets its own R worker and its own account.

```yaml
shiny_server__locations__group_var:
  - path: '/acme/app1'
    app_dir: '/srv/shiny-server/tenants/acme/app1'
    log_dir: '/var/log/shiny-server/acme'
    run_as: 'shiny-acme'
  - path: '/acme/app2'
    app_dir: '/srv/shiny-server/tenants/acme/app2'
    log_dir: '/var/log/shiny-server/acme'
    run_as: 'shiny-acme'
```

### 2. Declare one vHost per tenant

`locations` maps the URL path inside the vHost to the Shiny Server location behind it, so the tenant reaches its applications at `/app1` and `/app2` without the tenant name in the URL.

```yaml
shiny_server__vhosts__group_var:
  - conf_server_name: 'shiny-acme.example.com'
    htpasswd:
      - username: 'firstname.lastname'
        password: 'linuxfabrik'
    locations:
      - shiny_location: '/acme/app1'
        path: '/app1'
      - shiny_location: '/acme/app2'
        path: '/app2'
```

### 3. Lay out the application code

The role creates the directories; the files are yours to deploy. Symlink the shared code file by file so that the working directory of the R process stays the tenant directory:

```
/srv/shiny-server/shared/app1/app.R
/srv/shiny-server/tenants/acme/app1/app.R      -> ../../../shared/app1/app.R
/srv/shiny-server/tenants/acme/app1/config.R   (tenant specific)
/srv/shiny-server/tenants/acme/app1/data/      (tenant specific)
```


## Tags

`shiny_server`

* Installs Shiny Server.
* Creates the service account, the tenant accounts and the directory structure.
* Deploys the configuration, the systemd drop-in and the logrotate configuration.
* Ensures the service is in the desired state.
* Triggers: shiny-server.service reload, shiny-server.service restart.

`shiny_server:configure`

* Creates the directory structure and deploys the configuration and the systemd drop-in.
* Triggers: shiny-server.service reload, shiny-server.service restart.

`shiny_server:logrotate`

* Deploys the logrotate configuration of the application logs.
* Triggers: none.

`shiny_server:state`

* Manages the service state (start, stop, enable, disable).
* Triggers: none.

`shiny_server:users`

* Creates the accounts the applications run as.
* Triggers: none.


## Mandatory Role Variables

`shiny_server__version`

* The version of Shiny Server to install, as it appears in the package filename. Look it up on the [GitHub Tags page](https://github.com/rstudio/shiny-server/tags).
* Type: String.

Example:
```yaml
# mandatory
shiny_server__version: '1.5.23.1030'
```


## Optional Role Variables

`shiny_server__conf_allow_app_override`

* Allow an application directory to override server settings through a `.shiny_app.conf` next to the application code.
* Type: Bool.
* Default: `false`
* Deviates from the upstream default `true`: on a host where tenants own their application directories, this lets a tenant raise its own request limit, turn error sanitizing off, make its log files world readable and choose its own Python interpreter.

`shiny_server__conf_app_idle_timeout`

* Seconds an R process without a connection keeps running. `0` disables the cleanup. Keep it low for memory-hungry applications, otherwise abandoned sessions hold memory indefinitely.
* Type: Number.
* Default: `5`

`shiny_server__conf_app_init_timeout`

* Seconds an application is given to start.
* Type: Number.
* Default: `60`

`shiny_server__conf_frame_options`

* `X-Frame-Options` header sent on URLs served from Shiny applications, as a mitigation against clickjacking.
* Type: String. One of `allow`, `deny`, `sameorigin`.
* Default: `'sameorigin'`
* Deviates from the upstream default `allow`, which sends no header at all and lets any site embed the application in a frame.

`shiny_server__conf_http_keepalive_timeout`

* Seconds an HTTP connection stays open between requests.
* Type: Number.
* Default: `45`

`shiny_server__conf_listen_host`

* Address Shiny Server listens on. Leave this on the loopback: Shiny Server authenticates nobody and passes every client header through to the application, so any address reachable from the network is a way around the reverse proxy and its authentication.
* Type: String.
* Default: `'127.0.0.1'`
* Deviates from the upstream default `*`, which serves every interface.

`shiny_server__conf_listen_port`

* Port Shiny Server listens on.
* Type: Number.
* Default: `3838`

`shiny_server__conf_preserve_logs`

* Keep the log files of Shiny processes that exited successfully. Useful while hunting a startup error, together with the browser-only error message. Thousands of files accumulate quickly, which is why the role also rotates them.
* Type: Bool.
* Default: `false`

`shiny_server__conf_run_as`

* Account the applications run as unless a location names its own. This is the account the package creates.
* Type: String.
* Default: `'shiny'`

`shiny_server__conf_sanitize_errors`

* Send only generic error messages to the browser. Individual messages reach the user through `stop(safeError(e))` in the application code.
* Type: Bool.
* Default: `true`

`shiny_server__conf_simple_scheduler`

* Maximum number of concurrent requests per application before the server answers `503 Service Unavailable`. Lower it noticeably for applications that need a lot of memory.
* Type: Number.
* Default: `100`

`shiny_server__download_url`

* Full URL of the Shiny Server package. Empty derives it from `shiny_server__version` and the platform. Set it to install from a local mirror.
* Type: String.
* Default: `''`

`shiny_server__htpasswd_dir`

* Directory the per-tenant `.htpasswd` files are written to.
* Type: String.
* Default: `'/etc/httpd'`

`shiny_server__log_dir`

* Directory the application logs are written to, unless a location names its own.
* Type: String.
* Default: `'/var/log/shiny-server'`

`shiny_server__logrotate`

* Application log files are rotated `count` days before being removed.
* Type: Number.
* Default: `{{ logrotate__rotate | d(14) }}`

`shiny_server__memory_max`

* `MemoryMax` of the service. Shiny Server Open Source enforces no memory limit of its own, and a single R session can grow until the host is full without load or process count looking unusual. The R workers are started through `su` but stay in the control group of the service, so the cap reaches them. Empty leaves the setting out of the drop-in.
* Type: String.
* Default: `''`

`shiny_server__service_enabled`

* Enables or disables the service, analogous to `systemctl enable/disable --now`.
* Type: Bool.
* Default: `true`

`shiny_server__service_state`

* Changes the state of the service, analogous to `systemctl start/stop/restart/reload`.
* Type: String. One of `reloaded`, `restarted`, `started`, `stopped`.
* Default: `'started'`

`shiny_server__shared_dir`

* Directory holding the application code shared between the tenants. Readable for the accounts the applications run as through their membership in `shiny_server__shared_group`, invisible to the rest of the host.
* Type: String.
* Default: `'/srv/shiny-server/shared'`

`shiny_server__shared_group`

* Group that owns the shared code tree, and that every account an application runs as is a secondary member of. Keep it separate from `shiny_server__conf_run_as`: that account's group owns the application directory of every location left at the default `run_as`, so sharing one group for both purposes would let every tenant read those directories.
* Type: String.
* Default: `'shiny-shared'`

`shiny_server__site_dir`

* Root directory the role creates. `shiny_server__shared_dir` and `shiny_server__tenants_dir` live below it. The packaged Shiny Server serves this tree on `/`; this role does not, because it is handed out without any access control. A location with `site_dir` gives the same behaviour where it is actually wanted, behind the tenant's vHost.
* Type: String.
* Default: `'/srv/shiny-server'`

`shiny_server__tasks_max`

* `TasksMax` of the service, capping processes and threads in its control group. R forks for parallel work, so without it a runaway application is bounded only by systemd's `DefaultTasksMax`, which is 15% of `kernel.pid_max` and therefore commonly in the tens of thousands. Empty leaves the setting out of the drop-in.
* Type: Number.
* Default: `''`

`shiny_server__tenants_dir`

* Directory below which the per-tenant application directories live.
* Type: String.
* Default: `'/srv/shiny-server/tenants'`

`shiny_server__tmp_dir`

* `TMPDIR` of the R workers, injected into the `r` role. Shiny stores uploaded files in a per-session directory below `tempdir()` and refuses locations outside it, so this is where uploads land. Put it on its own partition where large uploads are expected, so that a full upload cannot fill the root file system. Shiny cleans the session directory up at the end of the session; where the R process dies first, the files stay behind, so data worth protecting needs a deletion concept of its own, for example with `systemd-tmpfiles`.
* Type: String.
* Default: `'/var/lib/shiny-server/tmp'`

`shiny_server__users_home_dir`

* Home directory root of the accounts the applications run as. Shiny Server does not start a worker whose account has no home directory.
* Type: String.
* Default: `'/var/lib/shiny-server/home'`

Example:
```yaml
# optional
shiny_server__conf_allow_app_override: false
shiny_server__conf_app_idle_timeout: 60
shiny_server__conf_app_init_timeout: 60
shiny_server__conf_frame_options: 'sameorigin'
shiny_server__conf_http_keepalive_timeout: 45
shiny_server__conf_listen_host: '127.0.0.1'
shiny_server__conf_listen_port: 3838
shiny_server__conf_preserve_logs: true
shiny_server__conf_run_as: 'shiny'
shiny_server__conf_sanitize_errors: true
shiny_server__conf_simple_scheduler: 20
shiny_server__download_url: 'https://mirror.example.com/shiny-server-1.5.23.1030-x86_64.rpm'
shiny_server__htpasswd_dir: '/etc/httpd'
shiny_server__log_dir: '/var/log/shiny-server'
shiny_server__logrotate: 7
shiny_server__memory_max: '8G'
shiny_server__service_enabled: true
shiny_server__service_state: 'started'
shiny_server__shared_dir: '/srv/shiny-server/shared'
shiny_server__shared_group: 'shiny-shared'
shiny_server__site_dir: '/srv/shiny-server'
shiny_server__tasks_max: 200
shiny_server__tenants_dir: '/srv/shiny-server/tenants'
shiny_server__tmp_dir: '/var/lib/shiny-server/tmp'
shiny_server__users_home_dir: '/var/lib/shiny-server/home'
```


## Optional Role Variables - Tenants

`shiny_server__locations__host_var` / `shiny_server__locations__group_var`

* The applications Shiny Server serves, one entry per tenant application. Each becomes a `location` and gets its own R worker.
* Type: List of dictionaries.
* Default: `[]`
* Subkeys:

    * `path`:

        * Mandatory. The request path Shiny Server serves this entry at.
        * Type: String.

    * `app_dir`:

        * Mandatory, unless `site_dir` is given. Directory of the Shiny application.
        * Type: String.

    * `site_dir`:

        * Optional, alternative to `app_dir`. Directory tree served as a website, containing applications and static files. Served without access control.
        * Type: String.
        * Default: unset, so the location serves the single application in `app_dir`

    * `log_dir`:

        * Optional. Directory the application logs are written to.
        * Type: String.
        * Default: the value of `shiny_server__log_dir`

    * `run_as`:

        * Optional. Account the application runs as. Naming one other than `shiny_server__conf_run_as` makes the role create it, which is what extends the separation into the file system.
        * Type: String.
        * Default: the value of `shiny_server__conf_run_as`

    * `app_idle_timeout`:

        * Optional. Seconds this application's R process keeps running without a connection.
        * Type: Number.
        * Default: the value of `shiny_server__conf_app_idle_timeout`

    * `app_init_timeout`:

        * Optional. Seconds this application is given to start.
        * Type: Number.
        * Default: the value of `shiny_server__conf_app_init_timeout`

    * `directory_index`:

        * Optional. List the directory contents when no `index.html` is present. Only meaningful together with `site_dir`.
        * Type: Bool.
        * Default: `false` (Shiny Server disables directory indexes when the directive is absent)

    * `python`:

        * Optional. Python interpreter or virtual environment for a Shiny for Python application.
        * Type: String.
        * Default: unset, so the location serves R applications

    * `sanitize_errors`:

        * Optional. Send only generic error messages to the browser.
        * Type: Bool.
        * Default: the value of `shiny_server__conf_sanitize_errors`

    * `simple_scheduler`:

        * Optional. Maximum number of concurrent requests before this application answers 503. Lower it for memory-hungry applications.
        * Type: Number.
        * Default: the value of `shiny_server__conf_simple_scheduler`

    * `state`:

        * Optional. `present` or `absent`. `absent` deletes the application directory including the tenant's data, the log directory, and the account the application ran as, unless another location still uses them. Removing the entry from the inventory instead only stops the location from being served and deletes nothing.
        * Type: String.
        * Default: `'present'`

`shiny_server__vhosts__host_var` / `shiny_server__vhosts__group_var`

* The Apache httpd vHosts, one entry per tenant. Injected into the `apache_httpd` role as a `proxy` vHost.
* Type: List of dictionaries.
* Default: `[]`
* Subkeys:

    * `conf_server_name`:

        * Mandatory. The tenant's hostname.
        * Type: String.

    * `locations`:

        * Mandatory. The applications this tenant reaches through this vHost.
        * Type: List of dictionaries.
        * Subkeys:

            * `shiny_location`:

                * Mandatory. The `path` of the `shiny_server__locations` entry behind it.
                * Type: String.

            * `path`:

                * Optional. The request path inside this vHost.
                * Type: String.
                * Default: the value of `shiny_location`

            * `state`:

                * Optional. `present` or `absent`.
                * Type: String.
                * Default: `'present'`

    * `htpasswd`:

        * Optional. The accounts allowed into this tenant's applications.
        * Type: List of dictionaries.
        * Subkeys:

            * `username`:

                * Mandatory. The login name.
                * Type: String.

            * `password`:

                * Mandatory for `state: 'present'`. The password.
                * Type: String.

            * `state`:

                * Optional. `present` or `absent`.
                * Type: String.
                * Default: the `state` of the vHost

    * `allowed_http_methods`:

        * Optional. The HTTP methods this vHost allows.
        * Type: List of strings.
        * Default: the value of `shiny_server__vhost_default_allowed_http_methods`

    * `auth_enabled`:

        * Optional. Protect this vHost with HTTP basic authentication.
        * Type: Bool.
        * Default: the value of `shiny_server__vhost_default_auth_enabled`

    * `auth_name`:

        * Optional. The realm shown in the browser's login prompt.
        * Type: String.
        * Default: `'Shiny <conf_server_name>'`

    * `auth_user_file`:

        * Optional. Path of this tenant's `.htpasswd` file.
        * Type: String.
        * Default: `'{{ shiny_server__htpasswd_dir }}/.htpasswd-<conf_server_name>'`

    * `conf_proxy_preserve_host`:

        * Optional. `ProxyPreserveHost` of this vHost.
        * Type: String.
        * Default: `'On'`

    * `conf_proxy_timeout`:

        * Optional. `ProxyTimeout` of this vHost, in seconds.
        * Type: Number.
        * Default: the value of `shiny_server__vhost_default_conf_proxy_timeout`

    * `credentials_header_enabled`:

        * Optional. Pass the authenticated user into the application, readable there as `session$user`.
        * Type: Bool.
        * Default: the value of `shiny_server__vhost_default_credentials_header_enabled`

    * `enabled`:

        * Optional. Whether the vHost is linked into `sites-enabled`.
        * Type: Bool.
        * Default: `true`

    * `filename`:

        * Optional. Filename of the vHost configuration.
        * Type: String.
        * Default: the value of `conf_server_name`

    * `raw`:

        * Optional. Verbatim Apache directives appended to this vHost, for TLS certificates and anything else the subkeys do not cover.
        * Type: String.
        * Default: `''`

    * `virtualhost_port`:

        * Optional. Port of this vHost.
        * Type: Number.
        * Default: the value of `shiny_server__vhost_default_virtualhost_port`

    * `state`:

        * Optional. `present` or `absent`.
        * Type: String.
        * Default: `'present'`

Example:
```yaml
# optional
shiny_server__locations__group_var:
  - path: '/acme/app1'
    app_dir: '/srv/shiny-server/tenants/acme/app1'
    log_dir: '/var/log/shiny-server/acme'
    run_as: 'shiny-acme'
    app_idle_timeout: 900
  - path: '/globex/app1'
    app_dir: '/srv/shiny-server/tenants/globex/app1'
    log_dir: '/var/log/shiny-server/globex'
    run_as: 'shiny-globex'
    simple_scheduler: 20
shiny_server__vhosts__group_var:
  - conf_server_name: 'shiny-acme.example.com'
    htpasswd:
      - username: 'firstname.lastname'
        password: 'linuxfabrik'
    locations:
      - shiny_location: '/acme/app1'
        path: '/app1'
  - conf_server_name: 'shiny-globex.example.com'
    virtualhost_port: 443
    htpasswd:
      - username: 'globex.admin'
        password: 'linuxfabrik'
    locations:
      - shiny_location: '/globex/app1'
        path: '/app1'
    raw: |
      SSLEngine on
      SSLCertificateFile /etc/pki/tls/certs/shiny-globex.example.com.crt
      SSLCertificateKeyFile /etc/pki/tls/private/shiny-globex.example.com.key
```


## Optional Role Variables - vHost Defaults

These apply to every generated vHost. Each can be overridden per vHost with the key of the same name without the `shiny_server__vhost_default_` prefix.

`shiny_server__vhost_default_allowed_http_methods`

* The HTTP methods the generated vHosts allow.
* Type: List of strings.
* Default: `['GET', 'HEAD', 'OPTIONS', 'POST']`
* `POST` is mandatory: file uploads and the SockJS fallback transports use it, and without it a `fileInput()` fails with a 405 the user interface does not explain. `HEAD` keeps header-only monitoring checks from answering 405.

`shiny_server__vhost_default_auth_enabled`

* Protect the generated vHosts with HTTP basic authentication.
* Type: Bool.
* Default: `true`

`shiny_server__vhost_default_conf_proxy_timeout`

* `ProxyTimeout` of the generated vHosts, in seconds. A WebSocket idles while R computes, and Apache drops it when this expires, which shows up in the browser as the application "greying out". Keep it above the longest expected computation.
* Type: Number.
* Default: `300`
* Deviates from the upstream default `60` (Apache's `Timeout`, which `ProxyTimeout` inherits when unset): a Shiny session carries no traffic while R works, so at the upstream value any computation longer than a minute kills the connection.

`shiny_server__vhost_default_credentials_header_enabled`

* Pass the user authenticated by Apache into the application through the `Shiny-Server-Credentials` header, where it is readable as `session$user`. Only safe because Shiny Server binds the loopback and the header is set, not added, so a value sent by the client is overwritten. This is not an authorization check: what the application does with the value is up to its own code.
* Type: Bool.
* Default: `true`

`shiny_server__vhost_default_virtualhost_port`

* Port of the generated vHosts.
* Type: Number.
* Default: `80`

Example:
```yaml
# optional
shiny_server__vhost_default_allowed_http_methods:
  - 'GET'
  - 'HEAD'
  - 'OPTIONS'
  - 'POST'
shiny_server__vhost_default_auth_enabled: true
shiny_server__vhost_default_conf_proxy_timeout: 900
shiny_server__vhost_default_credentials_header_enabled: true
shiny_server__vhost_default_virtualhost_port: 443
```


## Troubleshooting

**An application greys out a short while after it loads**

* The WebSocket was cut, usually by a timeout in the reverse proxy or a firewall in between. While R computes, no data flows over the connection and the proxy takes it for dead. Raise `conf_proxy_timeout` on the tenant's vHost above the longest expected computation.

**A file upload aborts and the browser console shows a 405**

* The reverse proxy does not let `POST` through, which is the only method Shiny accepts uploads on. Add it to `allowed_http_methods` on that vHost.

**An application fails to start and the error is only visible in the browser**

* The per-session logs below `/var/log/shiny-server/` are deleted once an application has started successfully. Set `shiny_server__conf_preserve_logs: true`, reload the service, and reproduce the error; the logs then stay.

**An application log reports `there is no package called '...'`**

* The R package is not installed in the system library, or the account the application runs as cannot read it. Check with `sudo --user=<run_as account> R --quiet -e ".libPaths()"` and add the package to `r__cran_packages__group_var`.

**The run aborts with `A vHost passes Shiny-Server-Credentials, but Shiny Server listens on ...`**

* The listener is reachable from the network, where a client can bypass Apache and set the identity header itself. Set `shiny_server__conf_listen_host` back to `127.0.0.1`, or turn the header off with `credentials_header_enabled: false` on the affected vHosts.

**`session$user` is empty in the application**

* The value arrives on the WebSocket upgrade request only, so `RequestHeader` must apply to it: the `early` flag would run the directive before authentication, and `%{REMOTE_USER}s` or `%{REMOTE_USER}e` both yield the literal `(null)`. The role writes the working form; a hand-written vHost has to use `expr=` as well.

**The service will not start and `/var/log/shiny-server.log` gains no new lines at all**

* systemd is refusing to run it. The unit ships `Restart=on-failure` with `StartLimitBurst=3` and `StartLimitInterval=45`, so after three failed starts within 45 seconds the process is no longer launched and therefore cannot log anything, which makes it look as though the log had stopped rather than the service. Clear it with `systemctl reset-failed shiny-server` and start again. The usual underlying cause is a configuration Shiny Server rejects; the reason for that is in the last lines the log did manage to write.

**Orphaned R processes after a restart**

* The unit uses `KillMode=process`, so systemd only stops the main process and leaves the workers to Shiny Server's own shutdown. Check with `systemctl status shiny-server` whether any survived.


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
