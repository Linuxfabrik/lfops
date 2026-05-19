# Ansible Role linuxfabrik.lfops.exoscale_vm

This role creates and manages instances (virtual machines) on [Exoscale](https://www.exoscale.com/). It also allows creating other compontents for the instance, such as networks and firewall rules.


*Available since LFOps `2.0.0`.*


## Known Limitations

* `exoscale_vm__service_offering` can only be changed within the same instance-type family (the Exoscale v2 API rejects cross-family scaling, e.g. `standard.tiny` to `memory.large`). To move across families, set `exoscale_vm__state: 'absent'`, re-run, then recreate.
* `exoscale_vm__disk_size` can only be grown, never shrunk (an Exoscale v2 API limit). Lowering the value will fail at `PUT /v2/instance/{id}:resize-disk`.
* Security-group rule idempotency relies on the v2 API returning the current `rules` array on `GET /v2/security-group/{id}`. If a future API version stops returning rules in that response, re-runs may attempt to create duplicate rules.
* `--check` only shows top-level changes accurately. Read-only GETs run normally (so `--check` reflects the live API state), but mutating calls are skipped without contacting the API, so downstream tasks that depend on a just-created resource (security-group rules after the SG is created, network attachments after the instance is created, the `:start` after a `:stop` for scale, etc.) silently skip in `--check`. Re-running `--check` after a successful real run gives a faithful diff because everything that needs to exist already does.
* `--diff` is supported on every mutating task: the diff shows the method, path, and JSON body that would be (or was) sent to the Exoscale API. `before` is empty for `POST`/`PUT` and contains the request summary for `DELETE`, so deletions render as removed lines.


## Mandatory Requirements

* Import your public SSH-key into Exoscale ([here](https://portal.exoscale.com/compute/keypairs)). Ideally, set the key name to your local username, then you can use the default value for `exoscale_vm__ssh_key`.
* No client binary or Python library is required on the Ansible control node. The role talks to the Exoscale [v2 HTTP API](https://openapi-v2.exoscale.com/) directly via the bundled `linuxfabrik.lfops.exoscale_api` module, which signs each request with `EXO2-HMAC-SHA256` using `exoscale_vm__api_key` / `exoscale_vm__api_secret`.


## Tags

`exoscale_vm`

* Creates and manages the instance.
* Triggers: none.

`exoscale_vm:firewalls`

* Manage the provider firewalls of the host.
* Triggers: none.

`exoscale_vm:networks`

* Manage the provider private networks.
* Triggers: none.


## Mandatory Role Variables

`exoscale_vm__api_key`

* Set the Exoscale API key. API keys can be managed [here](https://portal.exoscale.com/iam/api-keys). We recommend creating a unrestricted key, because else some operations fail.
* Type: String.

`exoscale_vm__api_secret`

* Set the Exoscale secret corresponding to the API key.
* Type: String.

`exoscale_vm__service_offering`

* The Exoscale service offering, in the form `<family>.<size>` (for example `standard.tiny`, `memory.extra-large`). This defines the amount of CPU cores and RAM. The available combinations can be obtained from the [v2 API](https://openapi-v2.exoscale.com/operation/operation-list-instance-types). Changing this value on an existing VM triggers `PUT /v2/instance/{id}:scale`; the role stops the VM first if needed, then leaves the post-state to `exoscale_vm__state` (which by default starts it again). Only within-family changes are accepted by the API (see Known Limitations).
* Type: String.

`exoscale_vm__template`

* The Exoscale template for the instance, either as a template name (looked up against `exoscale_vm__template_visibility`) or as a UUID (used directly without a lookup). The available templates can be obtained from the [v2 API](https://openapi-v2.exoscale.com/operation/operation-list-templates). Use the UUID when referencing custom (private) templates whose name is not unique.
* Type: String.

`exoscale_vm__zone`

* The Exoscale zone the instance should be in. Determines both the placement of the VM and the API endpoint (`https://api-{zone}.exoscale.com/v2`). Possible values include `at-vie-1`, `at-vie-2`, `bg-sof-1`, `ch-dk-2`, `ch-gva-2`, `de-fra-1`, `de-muc-1`, `hr-zag-1`.
* Type: String.

Example:
```yaml
# mandatory
exoscale_vm__api_key: 'EXOtn4Rg5ooosUALc1uNTqVTyTd'
exoscale_vm__api_secret: '4Is7jmDfzCONfJtEfxqX1VePSK9p7iZLafJy9ItC'
exoscale_vm__service_offering: 'standard.tiny'
exoscale_vm__template: 'Linux Rocky 9 (Blue Onyx) 64-bit'
exoscale_vm__zone: 'ch-dk-2'
```


## Optional Role Variables

`exoscale_vm__disk_size`

* The instance root disk size in GiB. Must be at least 10 and at most 51200 (Exoscale v2 limit). Increasing this value on an existing VM triggers `PUT /v2/instance/{id}:resize-disk`; the role stops the VM first if needed. The disk can only grow (see Known Limitations).
* Type: Number.
* Default: `10`

`exoscale_vm__name`

* The name of the instance. By default, the Ansible inventory name prefixed with `e` is used, as it has to start with a letter.
* Type: String.
* Default: `'e{{ inventory_hostname }}'`

`exoscale_vm__private_instance`

* Choose if the instance should be "private" without a public IP, or not.
* Type: Bool.
* Default: `true`

`exoscale_vm__private_networks`

* A list of dictionaries defining which private networks the instance should be attached to. The role reconciles the current attachment state against this list on every run:
    * Networks listed here but not currently attached are attached (`PUT /v2/private-network/{id}:attach`).
    * Networks currently attached but no longer in this list are detached (`PUT /v2/private-network/{id}:detach`).
    * For networks listed here with a `fixed_ip` whose current lease for this VM does not match, the lease is updated (`PUT /v2/private-network/{id}:update-ip`).
    * Networks listed with a `cidr` that do not yet exist are created (`POST /v2/private-network`). Existing networks are never destroyed by this role (a private network may be shared with other VMs).
* Type: List of dictionaries.
* Default: `[]`

* Subkeys:

    * `name`:

        * Mandatory. The name of an existing network, or the network which should be created.
        * Type: String.

    * `cidr`:

        * Optional. If this is given, a new network with this cidr is created if missing. Ignored when the network already exists.
        * Type: String.

    * `fixed_ip`:

        * Optional. The IPv4 address this VM should hold on the network. If the current lease for this VM on the network differs (or the VM was holding a DHCP-assigned address), the role calls `:update-ip` to switch to this address.
        * Type: String.

`exoscale_vm__security_group_rules`

* A list of dictionaries containing rules for the security group (basically Exoscale firewall rules).
* Type: List of dictionaries.
* Default: unset

* Subkeys:

    * `cidr`:

        * Optional. CIDR to be used for security group rule.
        * Type: String.

    * `protocol`:

        * Mandatory. To which IP protocol the rule is applied. Possible options: `tcp`, `udp`, `icmp`.
        * Type: String.

    * `start_port`:

        * Mandatory. The starting port.
        * Type: Number.

    * `end_port`:

        * Mandatory. The ending port.
        * Type: Number.

    * `state`:

        * Optional. State of the rule. Either `absent` or `present`.
        * Type: String.
        * Default: `'present'`

    * `type`:

        * Mandatory. For which direction the rule should apply. Possible options: `ingress`, `egress`.
        * Type: String.

`exoscale_vm__ssh_key`

* The name of the SSH-key deposited in Exoscale [here](https://portal.exoscale.com/compute/keypairs). Defaults to using the local username of the Ansible control node.
* Type: String.
* Default: `'{{ lookup("env", "USER") }}'`

`exoscale_vm__state`

* The desired state of the instance. Possible values:
    * `'started'` (default) or `'present'`: create the VM and ensure it is running. Calls `PUT /v2/instance/{id}:start` only if the current state is `stopped`.
    * `'stopped'`: create the VM with `auto-start: false` so it is not running on first boot. On subsequent runs, calls `PUT /v2/instance/{id}:stop` only if the current state is `running`.
    * `'restarted'`: same as `started`, but if the VM is already `running`, calls `PUT /v2/instance/{id}:reboot`. A fresh create with `'restarted'` behaves like `'started'` (no spurious reboot of a just-started VM). Leaving `'restarted'` in your inventory permanently means every Ansible run reboots the VM, which is usually not what you want.
    * `'absent'`: delete the VM, and the per-VM security group when `exoscale_vm__security_group_rules` is set.
* Type: String.
* Default: `'started'`

`exoscale_vm__template_visibility`

* Visibility under which `exoscale_vm__template` is looked up when given as a name. Use `'private'` for custom templates uploaded to your own account. Ignored when `exoscale_vm__template` is already a UUID.
* Type: String.
* Default: `'public'`

Example:
```yaml
# optional
exoscale_vm__disk_size: 10
exoscale_vm__name: '{{ inventory_hostname }}'
exoscale_vm__private_instance: false
exoscale_vm__private_networks:
  - name: 'net-prod01'
    cidr: '192.0.2.0/24'
    fixed_ip: '192.0.2.1'
exoscale_vm__security_group_rules:
  - type: 'ingress'
    protocol: 'tcp'
    start_port: 22
    end_port: 22
exoscale_vm__ssh_key: '{{ lookup("env", "USER") }}'
exoscale_vm__state: 'started'
exoscale_vm__template_visibility: 'private'
```


## Deprecated Role Variables

`exoscale_vm__account`

* No longer used. Previously identified which `exo` CLI / `~/.config/exoscale/exoscale.toml` profile to authenticate with. The role now signs every request itself with `exoscale_vm__api_key` / `exoscale_vm__api_secret`, so this variable is silently ignored. Kept in `meta/argument_specs.yml` so existing inventories that still set it do not fail role-entry validation.
* Type: String.


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
