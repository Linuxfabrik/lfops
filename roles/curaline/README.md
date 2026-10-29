# Ansible Role linuxfabrik.lfops.curaline

This role installs the curaLINE Client (`cdr-client`) of Swisscom, which exchanges files with the curaLINE Document Routing (CDR) service of the Swiss healthcare system, from the Linuxfabrik repository, and configures its connectors and folders. The client runs as the systemd service `swisscom-schweiz-ag-cdr-client.service` under the account `swisscom-schweiz-ag-cdr-client`, which the package creates.


*Available in the next LFOps release.*


## How the Role Behaves

* The package `swisscom-schweiz-ag-cdr-client` brings the client with its own Java runtime, the account, the default configuration and the systemd unit. Updates of the client come through the package manager.
* The role renders `/etc/swisscom-schweiz-ag/cdr-client/application-customer.yaml` on every run (a timestamped backup is kept), so manual edits are overwritten. This includes the client secret. The file belongs to `swisscom-schweiz-ag-cdr-client`, since the client refuses to start with a configuration it does not own.
* With `curaline__renew_credential: true` the client renews the secret and rewrites `application-customer.yaml` itself. The next run of the role restores the old secret and renewal time from the inventory, so the client immediately tries to renew again with a secret that is no longer valid, and its login is denied. Keep it at `false` and renew the secret by hand.
* The packaged unit runs the client sandboxed (`ProtectSystem=strict`): it may only write to its own directories below `/etc`, `/var/lib`, `/var/cache` and `/var/log`. The role adds the folders of the connectors (`source-folder`, `target-folder`, `source-archive-folder`) and `curaline__local_folder` to the drop-in `/etc/systemd/system/swisscom-schweiz-ag-cdr-client.service.d/read-write-paths.conf`.
* Missing folders are created for `swisscom-schweiz-ag-cdr-client:swisscom-schweiz-ag-cdr-client` with mode `2770`, so the accounts of the scripts that fill the source folders and empty the target folders get access by being added to the group `swisscom-schweiz-ag-cdr-client`. Existing folders keep their owner, mode and content, so they must already be writable by the account. Parent directories are created owned by `root`. The client creates the subfolders below them, such as `error`, itself.
* Files must be written to a source folder under a temporary name and renamed to `*.xml` when complete, and must be readable by `swisscom-schweiz-ag-cdr-client`. The client uploads a file that is still being written in fragments, and retries an unreadable file forever as `*.upload`.
* The role does not manage the firewall. The client only makes outgoing connections, and its management ports `8191` and `8193` listen on `127.0.0.1`.
* The client downloads a document into `curaline__local_folder` and then moves it to the target folder, so on the Red Hat family the file keeps the SELinux label of `curaline__local_folder` (`var_lib_t` by default). If a confined service such as Samba or httpd reads the target folder, put `curaline__local_folder` below the same tree as the target folder.


## Known Limitations

* Only `x86_64` hosts are supported.
* The role does not configure the proxy of the client.
* The role manages one client per host.


## Dependent Roles

Any [LFOps playbook](https://github.com/Linuxfabrik/lfops/blob/main/playbooks/README.md) that installs this role runs these for you. Optional ones can be disabled via the playbook's skip variables.

* The Linuxfabrik repository must be enabled (role: [linuxfabrik.lfops.repo_linuxfabrik](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_linuxfabrik)). The package of the client is served from it.


## Requirements

* Credentials for the curaLINE Document Routing service: the client ID and the client secret of the application registered for this client, and the connector ID(s) of the practice or institution.
* Outbound HTTPS access from the target to `cdr.health.swisscom.ch` and `login.microsoftonline.com`.


## Replacing the H-Net SecureClient

The SecureClient keeps its data in `/data/xml/{inbox,outbox,archive}` and their `-test` counterparts, owned by `hnet:hnet`. The curaLINE Client writes exactly into the configured folder, while the SecureClient appends the transaction type, so the folders of a connector end in `XMLDatenforum`, for example `/data/xml/outbox/XMLDatenforum`. Give `swisscom-schweiz-ag-cdr-client` access to the existing folders, for example by handing them to its group, or let the role create new ones.

**Warning:** Do not run both clients on the same folders. Both would pick up the files in the outbox, and documents could be sent twice or get lost. Stop and disable the SecureClient (`systemctl disable --now hnet-securesvc.service`) before the curaLINE Client is started for the first time, or deploy the role with `curaline__service_enabled: false` and `curaline__service_state: 'stopped'` until the switch-over.


## Post-Installation Steps

* Check the connection to the service: `curl --silent http://127.0.0.1:8193/actuator/health` no longer reports `"authN": {"status": "DENIED"}` once the credentials are accepted.


## Tags

`curaline`

* Installs the client.
* Creates the missing folders of the connectors.
* Deploys the configuration file and the systemd drop-in.
* Ensures the service is in the desired state.
* Triggers: swisscom-schweiz-ag-cdr-client.service restart.

`curaline:configure`

* Deploys the configuration file and the systemd drop-in.
* Triggers: swisscom-schweiz-ag-cdr-client.service restart.

`curaline:state`

* Manages the service state (start, stop, enable, disable).
* Triggers: none.


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

* Folder for temporary downloads. Do not point it below `/tmp`: the unit runs the client with `PrivateTmp=yes`, which empties `/tmp` on every stop and restart and would lose the documents being downloaded.
* Type: String.
* Default: `'/var/lib/swisscom-schweiz-ag/cdr-client'`

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
curaline__local_folder: '/var/lib/swisscom-schweiz-ag/cdr-client'
curaline__renew_credential: false
curaline__schedule_delay: 'PT10M'
curaline__service_enabled: true
curaline__service_state: 'started'
```


## Troubleshooting

**`curl http://127.0.0.1:8193/actuator/health` reports `"authN": {"status": "DENIED"}`**

* The identity provider rejects the credentials. Check `curaline__client_id`, `curaline__client_secret` and `curaline__tenant_id`. The client keeps running and retries, the reason is in `/var/log/swisscom-schweiz-ag/cdr-client/cdr-client-service.log`.

**The service fails with `status=226/NAMESPACE`**

* A path in `ReadWritePaths=` of the drop-in does not exist, typically a folder of a connector that was removed by hand, or one on a network share that is not mounted. Run the role again to recreate missing folders, or mount the share before the service starts.

**The run aborts with `At least one connector must be present ...` or `Connector ... must set content-type, source-folder and target-folder`**

* Give the host at least one connector in `curaline__connectors__host_var` or `curaline__connectors__group_var`, with all mandatory subkeys set.


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
