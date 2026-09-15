# Ansible Role linuxfabrik.lfops.rstudio_server

This role installs and configures [RStudio Server Open Source](https://posit.co/products/open-source/rstudio-server/), the browser-based R development environment from Posit.

RStudio Server authenticates against the accounts of the host through PAM and runs the R session of a signed-in user under that user's own account. The role installs and configures the service; the accounts themselves come from wherever the host gets its users.


*Available in the next LFOps release.*


## How the Role Behaves

* The package is downloaded on the Ansible controller and copied to the target, so targets without Internet access can be provisioned; the controller needs outbound access to `download2.rstudio.org`. It is fetched only when the installed version differs from `rstudio_server__version`.
* Posit signs its packages, so the role installs the RPM with the signature check on. The public key (`Posit Software, PBC <security-team@posit.co>`, fingerprint `8B65 E5A1 07BB EFE3 BA99 C597 51C0 B5BB 19F9 2D60`) ships with the role and is imported into the rpm keyring, because Posit publishes it on a web page and on the keyservers, but at no stable URL a task could fetch. It expires in May 2027 and has to be refreshed here before then.
* Posit builds one package per RHEL generation and publishes x86_64 only. RHEL 10 gets the RHEL 9 build: Posit publishes none for it, and the package needs nothing but `psmisc`, `sqlite` and `/bin/sh`, carrying its own Node.js and Boost below `/usr/lib/rstudio-server`.
* The configuration is deployed **before** the package. The package writes `rserver.conf`, `rsession.conf` and `/etc/pam.d/rstudio` only when none exists, and then enables and starts the service immediately, so without this the service would come up once on every interface with every account on the host allowed to sign in.
* Updating means raising `rstudio_server__version` and running the role again. The package manager resolves the file as an upgrade of the installed package, and a lower version as a downgrade. The package restarts the service as part of its own installation, which takes every running R session with it.
* `rserver` reads its configuration at startup only. `systemctl reload` sends `SIGHUP`, on which it re-reads the logging and the environment-variable configuration and nothing else, so the role restarts the service after a change to `rserver.conf`. The restart is preceded by a configuration check (`rserver --check-config`, or `--test-config` on releases that predate it), so a misspelled option aborts the run instead of leaving the service down. The check reports options `rserver` does not know; it does not validate their values, so a wrong value still surfaces at the restart.
* `rsession.conf` is read by each R session as it starts, and `/etc/pam.d/rstudio` on every sign-in, so neither needs a restart. A session that is already running keeps the settings it started with.
* The role does not create user accounts. It creates the group named in `rstudio_server__conf_auth_required_user_group` and lets `rserver` refuse everybody who is not a member. Deploy the accounts with the [login](https://github.com/Linuxfabrik/lfops/tree/main/roles/login) role, join the host to a directory with [freeipa_client](https://github.com/Linuxfabrik/lfops/tree/main/roles/freeipa_client), or bring them along however else the host gets its users.
* The role replaces the vendor's `/etc/pam.d/rstudio`, which authenticates against `pam_unix` alone and therefore knows neither a directory service nor `pam_faillock`. The role's file includes `password-auth`, the stack RHEL keeps for network services, so SSSD users can sign in and failed attempts are counted like everywhere else on the host. The package leaves an existing file alone, so this survives an update.
* RStudio Server Open Source never opens a PAM session, only `pam_authenticate()` and `pam_acct_mgmt()`. Nothing in the sign-in path creates a home directory, and a user whose home directory does not exist cannot work, so the accounts have to bring theirs along.
* On a host with SELinux enforcing, the `rserver` binary is labelled `bin_t`. Posit installs it below `/usr/lib`, where it carries `lib_t`, and systemd leaves a service whose binary is not `bin_t` in its own domain, `init_t`. From there the fork of a session is denied, so a user signs in and then waits forever for an R session that never starts, and the audit log holds `avc: denied { setpgid } for comm="rserver"`. The label moves the service into `unconfined_service_t`, the domain RHEL keeps for services that bring no policy of their own. The role applies the label with `restorecon`; the rule behind it comes from the `selinux` role.
* Both `rserver` and the R sessions log to syslog, which on these platforms is the journal (`journalctl --unit rstudio-server.service`). Nothing writes to a file, so the role deploys no logrotate configuration.
* The package overwrites `/usr/lib/systemd/system/rstudio-server.service` on every update, so unit settings go into a drop-in below `/etc/systemd/system/rstudio-server.service.d/` instead.
* The role does not manage TLS, the firewall or a reverse proxy. See "Known Limitations" for what that means in practice.


## Known Limitations

* RStudio Server Open Source speaks plain HTTP and has no TLS of its own (`ssl-enabled` is a Workbench option). The password does not travel in the clear, because the browser encrypts it with the server's public key before posting it, but everything else does, the session cookie included. A TLS-terminating reverse proxy in front is therefore part of the deployment, which is what the defaults assume. Marking the cookies as secure keeps a browser from signing in over the unencrypted port, but it is no access control: the attribute is enforced by the browser, and a client that replays the CSRF cookie itself is unaffected. Keeping that port off the network stays the job of the listen address and the firewall.
* Only the x86_64 package is supported. Posit publishes no aarch64 build.
* The resource limits in the systemd drop-in protect the host, not the individual session. All sessions of all users share the budget, and the OOM killer picks a process inside the control group when it is exceeded.
* A user with a shell in RStudio has the rights of their account on the host. The terminal, `system()` and R's own file functions all run as that user, so RStudio is not a sandbox: treat an account here like an SSH account on the same host.


## Dependent Roles

Any [LFOps playbook](https://github.com/Linuxfabrik/lfops/blob/main/playbooks/README.md) that installs this role runs these for you. Optional ones can be disabled via the playbook's skip variables.

* R must be installed (role: [linuxfabrik.lfops.r](https://github.com/Linuxfabrik/lfops/tree/main/roles/r)). `rserver` aborts at startup when it finds no R, and the package starts the service as part of its own installation, so the R installation has to be complete before this role runs.
* The EPEL repository must be enabled (role: [linuxfabrik.lfops.repo_epel](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_epel)), because R comes from there.
* On RHEL-compatible systems, the SELinux file context of the `rserver` binary must be set (roles: [linuxfabrik.lfops.policycoreutils](https://github.com/Linuxfabrik/lfops/tree/main/roles/policycoreutils), [linuxfabrik.lfops.selinux](https://github.com/Linuxfabrik/lfops/tree/main/roles/selinux)). Skipping them on a host with SELinux enforcing leaves a server nobody can start a session on.


## Requirements

* Outbound HTTPS access from the Ansible controller to `download2.rstudio.org`.

Manual steps:

* Look up the current version on the [RStudio Server download page](https://posit.co/download/rstudio-server/) and pin it in `rstudio_server__version`. It is the version as it appears in the package file name, for example `2026.08.2-200` in `rstudio-server-rhel-2026.08.2-200-x86_64.rpm`.
* Provide the user accounts, each with a home directory, and add them to the group in `rstudio_server__conf_auth_required_user_group`.
* Optional: put a TLS-terminating reverse proxy in front (roles [apache_httpd](https://github.com/Linuxfabrik/lfops/tree/main/roles/apache_httpd), [acme_sh](https://github.com/Linuxfabrik/lfops/tree/main/roles/acme_sh)) and open the port in the firewall (role [firewall](https://github.com/Linuxfabrik/lfops/tree/main/roles/firewall)).


## Tags

`rstudio_server`

* Installs RStudio Server.
* Creates the login group and deploys the configuration, the PAM profile and the systemd drop-in.
* Ensures the service is in the desired state.
* Triggers: rstudio-server.service restart.

`rstudio_server:configure`

* Deploys `rserver.conf`, `rsession.conf`, the PAM profile and the systemd drop-in.
* Triggers: rstudio-server.service restart.

`rstudio_server:state`

* Manages the service state (start, stop, enable, disable).
* Triggers: none.

`rstudio_server:users`

* Creates the group a user has to be a member of to sign in.
* Triggers: none.


## Mandatory Role Variables

`rstudio_server__version`

* The version of RStudio Server to install, as it appears in the package file name. Look it up on the [RStudio Server download page](https://posit.co/download/rstudio-server/).
* Type: String.

Example:
```yaml
# mandatory
rstudio_server__version: '2026.08.2-200'
```


## Optional Role Variables

`rstudio_server__conf_auth_cookies_force_secure`

* Mark the authentication cookies as secure, so that a browser sends them over HTTPS only. `rserver` does this by itself on an HTTPS connection and never has one, because RStudio Server Open Source speaks plain HTTP, so behind a TLS-terminating proxy this is the only way the flag is ever set.
* Type: Bool.
* Default: `true`
* Deviates from the upstream default `false`: the role assumes a TLS-terminating reverse proxy in front. Where users reach `rserver` over plain HTTP instead, set this to `false`, otherwise the browser withholds the cookies and no sign-in completes; see "Troubleshooting".

`rstudio_server__conf_auth_encrypt_password`

* Have the browser encrypt the password with the server's public key before posting it to the sign-in form. Turn it off only where a proxy in front mangles the form, and then only on a connection that carries TLS.
* Type: Bool.
* Default: `true`

`rstudio_server__conf_auth_minimum_user_id`

* Lowest user id allowed to sign in. `auto` reads `UID_MIN` from `/etc/login.defs`, which is 1000 on all supported platforms.
* Type: String or Number.
* Default: `'auto'`

`rstudio_server__conf_auth_required_user_group`

* Group a user has to be a member of to sign in. Comma-separated for several groups, empty to let every account on the host in. The role creates the group.
* Type: String.
* Default: `'rstudio-users'`
* Deviates from the upstream default `''`: without a group, every account on the host can sign in, including the service accounts of everything else running on it.

`rstudio_server__conf_auth_sign_in_throttle_seconds`

* Seconds a user has to wait before signing in again after signing out.
* Type: Number.
* Default: `5`

`rstudio_server__conf_auth_timeout_minutes`

* Minutes a user stays signed in while idle. `0` switches to RStudio's legacy behaviour, where the session lasts as long as the browser is open, or as many days as `auth-stay-signed-in-days` says when the user ticks "Stay signed in"; set that option through `rstudio_server__rserver_conf_raw` if you want it.
* Type: Number.
* Default: `60`

`rstudio_server__conf_limit_file_upload_size_mb`

* Maximum size of a file uploaded through the web interface, in MB. `0` lifts the limit. Uploads land in the user's home directory, so this is the guard against one user filling the file system from the browser.
* Type: Number.
* Default: `0`

`rstudio_server__conf_rsession_which_r`

* Path to the R program the sessions run, for example `/usr/lib64/R/bin/R`. Empty lets `rserver` find R itself, which works wherever R is on the `PATH`.
* Type: String.
* Default: `''`

`rstudio_server__conf_session_timeout_minutes`

* Minutes an idle session is kept before it is suspended or ended. `0` disables the timeout, which means an abandoned session holds its memory until the service restarts.
* Type: Number.
* Default: `120`

`rstudio_server__conf_session_timeout_suspend`

* Suspend the session when the timeout is reached instead of ending it. Suspending writes the workspace to disk and frees the memory; the user finds their variables again on the next sign-in.
* Type: Bool.
* Default: `true`

`rstudio_server__conf_www_address`

* Address `rserver` listens on. `0.0.0.0` covers a reverse proxy on another host; set it to `127.0.0.1` where the proxy runs on this one, so that nothing else can reach the service. Either way the port carries no TLS, so restrict who may connect to it.
* Type: String.
* Default: `'0.0.0.0'`

`rstudio_server__conf_www_enable_origin_check`

* Reject a request whose `Origin` names a host other than the one it was sent to.
* Type: Bool.
* Default: `true`
* Deviates from the upstream default `false`: it is what keeps another site from driving a signed-in browser session. Where a proxy in front rewrites the `Host` header, the origin no longer matches and this has to be turned off or the proxy has to pass the original host through.

`rstudio_server__conf_www_frame_origin`

* Origin allowed to embed RStudio in a frame. `none` allows no embedding at all.
* Type: String.
* Default: `'none'`

`rstudio_server__conf_www_port`

* Port `rserver` listens on.
* Type: Number.
* Default: `8787`

`rstudio_server__conf_www_root_path`

* Path prefix a proxy in front adds to the URL, so that RStudio knows what it is served as. Empty means the server is reached at `/`.
* Type: String.
* Default: `''`

`rstudio_server__conf_www_thread_pool_size`

* Threads serving incoming requests. A sign-in occupies one of them for as long as PAM takes, so a host with many users wants more than the default.
* Type: Number.
* Default: `6`

`rstudio_server__download_url`

* Full URL of the RStudio Server package. Empty derives it from `rstudio_server__version` and the platform. Set it to install from a local mirror.
* Type: String.
* Default: `''`

`rstudio_server__memory_max`

* `MemoryMax` of the service unit, for example `8G`. Empty leaves the setting out of the drop-in. Every signed-in user gets an R process of their own, and R holds its data in memory, so a single careless `read.csv()` can otherwise take the host down.
* Type: String.
* Default: `''`

`rstudio_server__pam_include`

* PAM stack `/etc/pam.d/rstudio` includes for authentication and account checks. `password-auth` is the stack RHEL keeps for network services and covers local accounts, SSSD and `pam_faillock`.
* Type: String.
* Default: `'password-auth'`

`rstudio_server__pam_minimum_uid`

* Lowest user id PAM lets through, checked before the password is. This is what keeps a stream of failed root sign-ins through the web interface from tripping `pam_faillock` on root and locking it out everywhere else on the host.
* Type: Number.
* Default: `1000`

`rstudio_server__rserver_conf_raw`

* Verbatim content appended to `rserver.conf`, for the options this role has no variable for. `rserver --help` lists them all.
* Type: String.
* Default: `''`

`rstudio_server__rsession_conf_raw`

* Verbatim content appended to `rsession.conf`, for the options this role has no variable for. `rsession --help` lists them all.
* Type: String.
* Default: `''`

`rstudio_server__service_enabled`

* Start `rstudio-server.service` at boot.
* Type: Bool.
* Default: `true`

`rstudio_server__service_state`

* Runtime state of `rstudio-server.service`. Note that `reloaded` re-reads the logging and environment-variable configuration only, not `rserver.conf`.
* Type: String. One of `reloaded`, `restarted`, `started`, `stopped`.
* Default: `'started'`

`rstudio_server__tasks_max`

* `TasksMax` of the service unit. Empty leaves the setting out of the drop-in. R forks for parallel work, and without a cap the host is bounded only by systemd's `DefaultTasksMax`, which is 15% of `kernel.pid_max`.
* Type: String.
* Default: `''`

Example:
```yaml
# optional
rstudio_server__conf_auth_required_user_group: 'rstudio-users'
rstudio_server__conf_auth_timeout_minutes: 60
rstudio_server__conf_www_address: '127.0.0.1'
rstudio_server__memory_max: '8G'
rstudio_server__tasks_max: 500
```


## Troubleshooting

**Sign-in answers "Temporary server error, please try again", and the journal says `Failed to validate sign-in with invalid CSRF form`**

* The browser reaches `rserver` over plain HTTP while `rstudio_server__conf_auth_cookies_force_secure` is on. Every cookie is then marked `secure`, the CSRF cookie included, so the browser withholds it and the check fails before the password is looked at. Put a TLS-terminating proxy in front, or set the variable to `false` for a deployment that deliberately runs without one.


**The service does not start, and the journal says `R doc dir (/usr/share/doc/R) not found`**

* `rserver` validates the R installation at startup and refuses to run without R's documentation directory. A host that installs packages with `tsflags=nodocs` in its `dnf.conf`, which many minimal and cloud images do, has R without it. Reinstall R with `dnf reinstall --setopt=tsflags= R`. The role checks this before it installs the package and aborts with the same advice.

**A user of the directory service cannot sign in, a local user can**

* The vendor's PAM profile authenticates against `pam_unix` only. Check that `/etc/pam.d/rstudio` is the one this role deploys and that `rstudio_server__pam_include` names a stack that includes `pam_sss`.

**A user with the right password is refused, and the journal says `they do not belong to one of the required groups`**

* The account is not a member of the group in `rstudio_server__conf_auth_required_user_group`. Add it there; a new membership takes effect on the next sign-in, without restarting anything.

**A user signs in, the browser then waits and no session appears**

* Check `journalctl --unit rstudio-server.service` for `exited with status 256 before a connection was made`. On an enforcing host this is the missing `bin_t` label on `/usr/lib/rstudio-server/bin/rserver`: `ps -eZ | grep rserver` shows the service in `init_t` instead of `unconfined_service_t`. Run the role with the `selinux` role enabled, or set the context by hand with `semanage fcontext --add --type bin_t /usr/lib/rstudio-server/bin/rserver`, `restorecon -v /usr/lib/rstudio-server/bin/rserver` and a restart of the service. The matching denial is `avc: denied { setpgid } for comm="rserver" ... tclass=process` in `/var/log/audit/audit.log`.


**`rstudio-server verify-installation` reports `Server is running and must be stopped before running verify-installation`**

* That command starts a server of its own and therefore needs the port. Stop the service, run it, start the service again.


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
