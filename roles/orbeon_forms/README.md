# Ansible Role linuxfabrik.lfops.orbeon_forms

This role deploys [Orbeon Forms](https://www.orbeon.com/) (Community Edition) into an existing Apache Tomcat and wires it up specifically for the Numishare stack: Numishare's `apps/` symlink, eXist-db XQJ libraries, container-managed authentication for Numishare's roles, the `/themes/*` servlet mapping, and the discovery + delivery symlinks against `/opt/themes`.

The role:

* Downloads the Orbeon CE release zip from `orbeon_forms__zip_url` and extracts `orbeon.war` exploded into `orbeon_forms__home` (default `/var/lib/tomcat/webapps/orbeon`). Tomcat then picks it up as the `/orbeon` webapp.
* Rewrites `WEB-INF/resources/config/log4j2.xml` to absolute log paths under `orbeon_forms__log_dir` (default `/var/log/tomcat`). Orbeon's relative `../logs/` paths resolve to `/usr/share/logs/` on RHEL 10 Tomcat, where the `tomcat` user can not create files; the FileAppenders silently fail and surface only as generic "Page Not Found" responses.
* Deploys `Catalina/localhost/orbeon.xml` with `allowLinking="true"` so Tomcat follows the symlinks the role creates. The `path` attribute is intentionally omitted (Tomcat ignores it for context descriptors and emits a warning).
* Symlinks `numishare` → `<orbeon_home>/WEB-INF/resources/apps/numishare` and copies the eXist-db XQJ libraries from `<numishare>/vendor/exist-xqj-api-1.0.1/*.jar` into `<orbeon_home>/WEB-INF/lib/`.
* Provides a Numishare-branded favicon at `<orbeon_home>/WEB-INF/resources/ops/images/orbeon-icon-16.{ico,png}` (Numishare's xforms templates hardcode that path; Orbeon 2023.1 dropped the file from the WAR).
* Copies `properties-local.xml.template` to `properties-local.xml` and injects a managed Numishare block via `blockinfile` markers (epilogue theme, container auth method and roles).
* Replaces Orbeon's shipped `<login-config>` with a configurable BASIC or FORM auth block, replaces `<session-config>` with `orbeon_forms__session_timeout`, and injects a managed Numishare block before `</web-app>` (security-constraint for `/numishare/admin/*`, security-roles, and the `/themes/*` default-servlet mapping).
* Wires `orbeon_forms__themes_dir` (default `/opt/themes`) into Orbeon as both the discovery path (`<orbeon_home>/WEB-INF/resources/apps/themes`) and the delivery path (`<orbeon_home>/themes`).
* Recursively `chown`s `<orbeon_home>` to the Tomcat user/group and restarts Tomcat.


*Available in the next LFOps release.*


## Dependent Roles

Any [LFOps playbook](https://github.com/Linuxfabrik/lfops/blob/main/playbooks/README.md) that installs this role runs these for you. Optional ones can be disabled via the playbook's skip variables.

* Apache Tomcat must be installed and running, with the `tomcat` user/group present (role: [linuxfabrik.lfops.apache_tomcat](https://github.com/Linuxfabrik/lfops/tree/main/roles/apache_tomcat)).
* Numishare must be checked out at `orbeon_forms__numishare_dir` (role: [linuxfabrik.lfops.numishare](https://github.com/Linuxfabrik/lfops/tree/main/roles/numishare)).


## Requirements

* Container roles must be configured in `apache_tomcat__roles__*` with matching `apache_tomcat__users__*` entries, so that the BASIC/FORM-auth login against `/numishare/admin/*` works.


## Tags

`orbeon_forms`

* Installs `unzip`, deploys the WAR, fixes the log paths, deploys `orbeon.xml`, wires Numishare and themes, injects properties / web.xml blocks, and restarts Tomcat.


## Mandatory Role Variables

None. All variables have defaults that match the Numishare stack layout.


## Optional Role Variables

`orbeon_forms__auth_method`

* HTTP authentication method written into the Orbeon `web.xml`.
* Type: String. One of `'BASIC'` or `'FORM'`.
* Default: `'BASIC'`

`orbeon_forms__form_error_page`

* Login-failure page when `auth_method == 'FORM'`. Numishare ships `/numishare/login-failed`.
* Type: String.
* Default: `'/numishare/login-failed'`

`orbeon_forms__form_login_page`

* Login page when `auth_method == 'FORM'`. Numishare ships `/numishare/login`.
* Type: String.
* Default: `'/numishare/login'`

`orbeon_forms__home`

* Exploded-WAR deployment directory. Tomcat must scan this path for webapps.
* Type: String.
* Default: `'/var/lib/tomcat/webapps/orbeon'`

`orbeon_forms__log_dir`

* Absolute path that replaces Orbeon's shipped `../logs/` references in `log4j2.xml`. Must be writable by the Tomcat user; the default matches the Tomcat-package convention so the role's logrotate config covers Orbeon logs as well.
* Type: String.
* Default: `'/var/log/tomcat'`

`orbeon_forms__numishare_dir`

* Where Numishare is checked out. Must match `numishare__install_dir`.
* Type: String.
* Default: `'/opt/numishare'`

`orbeon_forms__roles`

* Container roles allowed to access `/numishare/admin/*`. Each entry must have a matching `apache_tomcat__roles__*` and `apache_tomcat__users__*` entry so login actually works. The default ships only the universal `numishare-admin` role; per-collection roles are added via the inventory.
* Type: List of strings.
* Default: `['numishare-admin']`

`orbeon_forms__session_timeout`

* Replaces Orbeon's shipped `<session-config>` value. Numishare's admin forms benefit from a higher timeout because configuration runs are long.
* Type: Number (minutes).
* Default: `720`

`orbeon_forms__themes_dir`

* Theme root directory exposed as the `apps/themes` discovery path and the `<orbeon_home>/themes` delivery path.
* Type: String.
* Default: `'/opt/themes'`

`orbeon_forms__tomcat_conf_dir`

* Tomcat configuration root. The role writes `<orbeon_forms__tomcat_conf_dir>/Catalina/localhost/orbeon.xml`.
* Type: String.
* Default: `'/usr/share/tomcat/conf'`

`orbeon_forms__tomcat_group`

* Group that owns Orbeon's deployment files. Must match the Tomcat group.
* Type: String.
* Default: `'tomcat'`

`orbeon_forms__tomcat_user`

* User that owns Orbeon's deployment files. Must match the Tomcat user.
* Type: String.
* Default: `'tomcat'`

`orbeon_forms__version`

* Orbeon CE version. Used to construct the download URL and identify the local copy under `/tmp`.
* Type: String.
* Default: `'2023.1.202312312000'`

`orbeon_forms__zip_url`

* Direct download URL of the Orbeon CE zip. The role unpacks `orbeon.war` from inside the zip and explodes it.
* Type: String.
* Default: `'https://github.com/orbeon/orbeon-forms/releases/download/tag-release-2023.1-ce/orbeon-2023.1.202312312000-CE.zip'`


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
