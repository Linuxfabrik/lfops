# Ansible Role linuxfabrik.lfops.curaline

This role installs and configures the curaLINE Client (`cdr-client`) of Swisscom, which exchanges files with the curaLINE Document Routing (CDR) service of the Swiss healthcare system. It unpacks the client from the Swisscom download page, configures its connectors and runs it as the systemd service `cdr-client.service` under a system account of its own.


*Available in the next LFOps release.*


## How the Role Behaves

* The client is downloaded on the Ansible controller (`delegate_to: 'localhost'`) into `/tmp` and uploaded to the target, so targets without Internet access can still be provisioned. The controller needs outbound HTTPS access to `cdr.health.swisscom.ch`. The target needs it only for the client to do its work.
* The client comes with its own Java runtime and is only published for `linux-amd64`. The role aborts on other architectures.
* The installed version is recorded in `/usr/lib/swisscom-schweiz-ag/cdr-client/.ansible-version`. When it differs from `curaline__version`, the role removes `/usr/lib/swisscom-schweiz-ag/cdr-client`, unpacks the new version and restarts the service. The configuration lives in `/etc/swisscom-schweiz-ag/cdr-client` and survives the update.
* The installation directory belongs to the `curaline` account, because the client writes to it while it runs, for example its `.cache`.
* The folders of the connectors (`source-folder`, `target-folder`, `source-archive-folder`) and `curaline__local_folder` are created and handed to `curaline` without touching their content. Parent directories are created owned by `root`. The client creates the subfolders below them, such as `error`, itself.
* The files in `/etc/swisscom-schweiz-ag/cdr-client` are re-rendered on every run (a timestamped backup is kept), so manual edits are overwritten. This includes the client secret in `application-customer.yaml`.
* With `curaline__renew_credential: true` the client replaces the client secret in `application-customer.yaml` by itself, and the next run of the role sets the one from the inventory again. Leave it at `false` unless the secret in the inventory is renewed by hand.
* The role does not manage the firewall. The client only makes outgoing connections, and its management ports `8191` and `8193` listen on `127.0.0.1`.
* On the Red Hat family with SELinux, the role sets the `bin_t` file context on `/usr/lib/swisscom-schweiz-ag/cdr-client/bin`, so that systemd may execute the client from `/usr/lib`.


## Known Limitations

* Only `x86_64` hosts are supported.
* The role does not configure the proxy of the client.
* The role manages one client per host.


## Requirements

* Credentials for the curaLINE Document Routing service: the client ID and the client secret of the application registered for this client, and the connector ID(s) of the practice or institution.
* Outbound HTTPS access from the Ansible controller to `cdr.health.swisscom.ch`, and from the target to `cdr.health.swisscom.ch` and `login.microsoftonline.com`.


## Post-Installation Steps

* Check the connection to the service: `curl --silent http://127.0.0.1:8193/actuator/health` no longer reports `"authN": {"status": "DENIED"}` once the credentials are accepted.


## Tags

`curaline`

* Installs the required packages.
* Creates the curaline system user and group, and the folders of the connectors.
* Installs the client.
* Deploys the configuration files and the systemd unit.
* Sets the SELinux file context of the client (Red Hat family with SELinux).
* Ensures the service is in the desired state.
* Triggers: cdr-client.service restart.

`curaline:configure`

* Deploys the configuration files and the systemd unit.
* Sets the SELinux file context of the client (Red Hat family with SELinux).
* Triggers: cdr-client.service restart.

`curaline:state`

* Manages the service state (start, stop, enable, disable).
* Triggers: none.

`curaline:update`

* Installs the client in the version of `curaline__version`, if it is not installed yet.
* Sets the SELinux file context of the client (Red Hat family with SELinux).
* Triggers: cdr-client.service restart.


## Mandatory Role Variables

`curaline__client_id`

* The client ID of the application registered for this client.
* Type: String.

`curaline__client_secret`

* The client secret that belongs to the client ID.
* Type: String.

`curaline__connectors__host_var` / `curaline__connectors__group_var`

* The connectors of the client. At least one must be present. Items are identified by the combination of `connector-id` and `mode`, so the same connector can run in `test` and `production` mode at once.
* Type: List of dictionaries.
* Default: `[]`
* Subkeys:

    * `connector-id`:

        * Mandatory. The ID of the connector, assigned by Swisscom.
        * Type: Number.

    * `mode`:

        * Mandatory. `production` or `test`.
        * Type: String.

    * `content-type`:

        * Mandatory. The content type of the documents.
        * Type: String.

    * `source-folder`:

        * Mandatory. The folder the client uploads documents from.
        * Type: String.

    * `target-folder`:

        * Mandatory. The folder the client puts downloaded documents into.
        * Type: String.

    * `source-archive-enabled`:

        * Optional. Whether the client moves uploaded documents to `source-archive-folder`.
        * Type: Bool.

    * `source-archive-folder`:

        * Optional. The folder for uploaded documents.
        * Type: String.

    * `state`:

        * Optional. `present` or `absent`. A connector set to `absent` is removed from the configuration, and its folders are not created.
        * Type: String.
        * Default: `'present'`

    * Any other key the client knows is written to the configuration as it is.

`curaline__version`

* The version of the curaLINE Client to install.
* Type: String.

Example:
```yaml
# mandatory
curaline__client_id: 'linuxfabrik'
curaline__client_secret: 'linuxfabrik'
curaline__connectors__host_var:
  - connector-id: 40000
    mode: 'test'
    content-type: 'application/forumdatenaustausch+xml;charset=UTF-8'
    source-folder: '/data/xml/outbox-test/XMLDatenforum'
    target-folder: '/data/xml/inbox-test/XMLDatenforum'
    source-archive-enabled: true
    source-archive-folder: '/data/xml/archive-test'
curaline__version: '6.2.1'
```


## Optional Role Variables

`curaline__cdr_api_base_path`

* Base path of the curaLINE document API.
* Type: String.
* Default: `'api/documents'`

`curaline__cdr_api_host`

* Host name of the curaLINE API.
* Type: String.
* Default: `'cdr.health.swisscom.ch'`

`curaline__cdr_api_port`

* Port of the curaLINE document API.
* Type: Number.
* Default: `443`

`curaline__cdr_api_scheme`

* Scheme of the curaLINE document API. One of `http`, `https`.
* Type: String.
* Default: `'https'`

`curaline__credential_api_base_path`

* Base path of the curaLINE credential API.
* Type: String.
* Default: `'api/client-credentials'`

`curaline__credential_api_host`

* Host name of the curaLINE credential API.
* Type: String.
* Default: `{{ curaline__cdr_api_host }}`

`curaline__credential_api_port`

* Port of the curaLINE credential API.
* Type: Number.
* Default: `{{ curaline__cdr_api_port }}`

`curaline__credential_api_scheme`

* Scheme of the curaLINE credential API. One of `http`, `https`.
* Type: String.
* Default: `{{ curaline__cdr_api_scheme }}`

`curaline__file_busy_test_strategy`

* How the client decides that a file in a source folder is completely written. `file_size_changed` samples the file size, `never_busy` takes every file as finished, `always_busy` never uploads.
* Type: String. One of `always_busy`, `file_size_changed`, `never_busy`.
* Default: `'file_size_changed'`

`curaline__file_synchronization_enabled`

* Whether the client uploads and downloads files.
* Type: Bool.
* Default: `true`

`curaline__idp_endpoint`

* The OAuth2 token endpoint of the identity provider.
* Type: String.
* Default: `'https://login.microsoftonline.com/{{ curaline__tenant_id }}/oauth2/v2.0/token'`

`curaline__last_credential_renewal_time`

* When the client credential was last renewed. A time in the past makes the client renew it on start, if `curaline__renew_credential` is enabled.
* Type: String.
* Default: `'1970-01-01T00:00:00Z'`

`curaline__local_folder`

* Folder for temporary downloads.
* Type: String.
* Default: `'/data/cdr-inflight'`

`curaline__renew_credential`

* Whether the client renews its client secret on its own, see "How the Role Behaves".
* Type: Bool.
* Default: `false`
* Deviates from the upstream default `true`: with it the client rewrites `application-customer.yaml` on its own, which the next run of the role would undo.

`curaline__schedule_delay`

* Interval between two upload and download runs, as an ISO 8601 duration.
* Type: String.
* Default: `'PT10M'`

`curaline__scope`

* The OAuth2 scope of the token request.
* Type: String.
* Default: `'https://identity.health.swisscom.ch/CdrApi/.default'`

`curaline__service_enabled`

* Enables or disables the service, analogous to `systemctl enable/disable --now`.
* Type: Bool.
* Default: `true`

`curaline__service_state`

* Changes the state of the service, analogous to `systemctl start/stop/restart`.
* Type: String. One of `restarted`, `started`, `stopped`.
* Default: `'started'`

`curaline__tenant_id`

* The Entra ID tenant that issues the tokens. The default is the tenant of Swisscom, which the client ships with.
* Type: String.
* Default: `'70b434db-eccb-4280-95dc-1e59220aca55'`

Example:
```yaml
# optional
curaline__cdr_api_base_path: 'api/documents'
curaline__cdr_api_host: 'cdr.health.swisscom.ch'
curaline__cdr_api_port: 443
curaline__cdr_api_scheme: 'https'
curaline__credential_api_base_path: 'api/client-credentials'
curaline__file_busy_test_strategy: 'file_size_changed'
curaline__file_synchronization_enabled: true
curaline__local_folder: '/data/cdr-inflight'
curaline__renew_credential: false
curaline__schedule_delay: 'PT10M'
curaline__service_enabled: true
curaline__service_state: 'started'
```


## Troubleshooting

**`curl http://127.0.0.1:8193/actuator/health` reports `"authN": {"status": "DENIED"}`**

* The identity provider rejects the credentials. Check `curaline__client_id`, `curaline__client_secret` and `curaline__tenant_id`. The client keeps running and retries, the reason is in `/var/log/cdr-client/cdr-client-service.log`.

**The run aborts with `curaline__version must look like "6.2.1", at least one connector must be present ...`**

* Set `curaline__version` to a release listed on the curaLINE download page, and give the host at least one connector in `curaline__connectors__host_var` or `curaline__connectors__group_var`.


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
