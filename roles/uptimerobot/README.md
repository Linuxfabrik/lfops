# Ansible Role linuxfabrik.lfops.uptimerobot

This role applies a declarative UptimeRobot configuration (monitors, maintenance windows, public status pages, and alert-contact cleanup) against an [UptimeRobot](https://uptimerobot.com/) account.


## What is UptimeRobot

UptimeRobot is a hosted uptime-monitoring service. You configure *monitors* (HTTP / keyword / port / ping / heartbeat checks), wire them up to *alert contacts* (email, SMS, webhook, Slack, ...), schedule *maintenance windows* during which alerts are suppressed, and optionally publish a *public status page* (PSP) that aggregates a set of monitors. Everything lives in UptimeRobot's cloud — there is no agent on your hosts.

The role does not deploy any software on the target hosts. It runs on the Ansible controller, talks to the UptimeRobot HTTP API, and brings the account into the desired state. Run it on `localhost` (or any host that has outbound HTTPS to `api.uptimerobot.com`).


## Concepts

The role works with five concepts that map 1:1 to UptimeRobot's data model and to one Ansible CRUD module each (plus a parallel set of read-only `*_info` modules — see the migration section below):

* **Monitor** (`linuxfabrik.lfops.uptimerobot_monitor`) — a single check (URL, host, heartbeat). Carries its own interval, timeout, HTTP method, optional auth, optional keyword search, and references to alert contacts and maintenance windows.
* **Maintenance window** (`linuxfabrik.lfops.uptimerobot_mwindow`) — a recurring or one-off time slot in which monitors that reference it stop alerting. `daily`, `weekly`, `monthly`, or `once`.
* **Public Status Page / PSP** (`linuxfabrik.lfops.uptimerobot_psp`) — a public web page that shows the current state of a hand-picked subset of monitors. Optional custom domain, optional password.
* **Alert contact** (`linuxfabrik.lfops.uptimerobot_alert_contact`) — a notification target (email address, SMS number, webhook, ...). UptimeRobot's API does not allow creating or editing contacts; the module is therefore *delete-only* and used to clean up stale contacts. Add new contacts in the UptimeRobot web UI.
* **Account** (`linuxfabrik.lfops.uptimerobot_account_info`) — read-only. Returns account-level facts (email, monitor quota, current monitor counters, SMS credits, ...).

The role chains the four CRUD modules in the right order: maintenance windows first, then monitors (which can reference windows by name), then PSPs (which reference monitors by name), finally the alert-contact cleanup.

The modules currently target UptimeRobot API v2 (POST + form-urlencoded). The full reference for that API — endpoint paths, parameters, return shapes, enumerations — lives at <https://uptimerobot.com/api/legacy/>. A future migration to API v3 stays local to `plugins/module_utils/uptimerobot.py` and does not change the role's variables or task layout.


## API Limits and Wire-Format Quirks

UptimeRobot's API has a few sharp edges that are useful to know up front. The modules absorb most of them, but the limits affect playbook design.

* **Rate limits** are per API key:
    * Free plan: 10 requests/minute.
    * Pro plan: `monitor_limit × 2` requests/minute, capped at 5000/min.
    * On HTTP 429 the response carries `X-RateLimit-Limit`, `X-RateLimit-Remaining`, `X-RateLimit-Reset` and `Retry-After`. The wrapper sleeps for `Retry-After` (capped at 60s) and retries once; a second 429 fails the task with the rate-limit headers in the message. For inventories with hundreds of monitors, run the role serially (no `serial:` / no `forks` against `localhost`) and consider a Pro key.
* **Pagination**: `getMonitors` and friends return at most 50 items per page. The wrapper pages through automatically.
* **`custom_http_headers`** is sent as a JSON object — pass it as a dict in the inventory or as a JSON string. The wrapper does not parse / validate the contents.
* **`custom_http_statuses`** uses an UptimeRobot-specific wire format: `'<code>:<flag>_<code>:<flag>'`, e.g. `'404:0_200:1'`. Underscore-separated pairs, colon between status and flag (1 = treat as up, 0 = treat as down).
* **`alert_contacts`** is *not* exposed as a JSON list to the wire; it is a string of the form `id_threshold_recurrence-id_threshold_recurrence`. The role builds that string from the `friendly_name` / `id`, `threshold`, `recurrence` items in your inventory, so you never write the wire form by hand.
* **`mwindows`** is a dash-separated string of IDs (`12345-67890`); same story — the role builds it from `friendly_name` / `id`.
* **PSP `monitors`** is comma-separated (`12345,67890`); ditto.
* **Alert contacts** can only be created and edited through the UptimeRobot web UI. The API exposes delete only.
* **Monitor `type` is immutable** — UptimeRobot will not change a monitor's type after creation. Recreate the monitor (`state: 'absent'` then `state: 'present'`) if you need to switch.


## Tags

`uptimerobot`

* Runs everything: maintenance windows, then monitors, then public status pages, then alert-contact cleanup.
* Triggers: none.

`uptimerobot:mwindow`

* Apply maintenance windows only.

`uptimerobot:monitor`

* Apply monitors only. Maintenance windows referenced by name must already exist.

`uptimerobot:psp`

* Apply public status pages only. Monitors referenced by name must already exist.

`uptimerobot:alert_contact`

* Delete the listed alert contacts only.


## Mandatory Requirements

* An UptimeRobot account.
* An UptimeRobot API key with write access (account-wide). Pass it via `uptimerobot__api_key`, via `uptimerobot__api_key_file` (default `~/.uptimerobot`), or via the `UPTIMEROBOT_API_KEY` environment variable. The modules try those three sources in that order.
* Outbound HTTPS from the controller to `https://api.uptimerobot.com/`.


## Optional Role Variables

`uptimerobot__api_key`

* UptimeRobot API key. If empty, the modules fall back to `uptimerobot__api_key_file` and finally to the `UPTIMEROBOT_API_KEY` environment variable. The Bitwarden lookup plugin (`linuxfabrik.lfops.bitwarden_item`) is the recommended way to populate this in production inventories.
* Type: String.
* Default: `''`

`uptimerobot__api_key_file`

* Path to a file containing the API key. Convenient for workstation use.
* Type: String.
* Default: `''` (the modules then probe `~/.uptimerobot`).

`uptimerobot__monitors`

* List of monitors to manage. The role synthesises each monitor's `friendly_name` as `'<prefix> <url-without-protocol>'` (a Linuxfabrik convention to keep monitor names self-documenting and groupable). To use a literal name instead, pass `friendly_name` directly.
* Type: List of dictionaries.
* Default: `[]`

* Subkeys (anything accepted by `linuxfabrik.lfops.uptimerobot_monitor` is honoured):

    * `prefix`:

        * Optional. Customer / project / inventory prefix that gets prepended to the synthesised `friendly_name`.
        * Type: String.

    * `url`:

        * Mandatory. URL or host or heartbeat token to monitor. Has to be unique across all your monitors.
        * Type: String.

    * `friendly_name`:

        * Optional. Takes precedence over the synthesised name.
        * Type: String.

    * `type`:

        * Optional. `'http'` (default), `'keyw'` (keyword check), `'ping'` (ICMP), `'port'` (TCP port), `'beat'` (heartbeat). Only honoured on create — UptimeRobot does not allow changing the type after creation.
        * Type: String.

    * `sub_type`:

        * Optional. For `type: 'port'`: which protocol/port preset (`'http'`, `'https'`, `'ftp'`, `'smtp'`, `'pop3'`, `'imap'`, `'custom'`). `'custom'` means "use the explicit `port` value".
        * Type: String.

    * `port`:

        * Optional. Custom TCP port for `type: 'port'` + `sub_type: 'custom'`.
        * Type: Number.

    * `keyword_type` / `keyword_case_type` / `keyword_value`:

        * Optional. For `type: 'keyw'`. `keyword_type` is `'exist'` (alert when keyword is present) or `'notex'` (alert when keyword is missing). `keyword_case_type` is `'cs'` or `'ci'`. `keyword_value` is the literal string searched for in the response body.
        * Type: String.

    * `interval`:

        * Optional. Check interval in seconds. UptimeRobot enforces a per-plan minimum (e.g. 30s on Pro).
        * Type: Number.

    * `timeout`:

        * Optional. Per-check timeout in seconds.
        * Type: Number.

    * `status`:

        * Optional. `'up'` un-pauses the monitor, `'paused'` pauses it. Only honoured on update.
        * Type: String.

    * `http_method`:

        * Optional. HTTP method for HTTP(S) monitors (`'get'`, `'head'`, `'post'`, `'put'`, `'patch'`, `'delete'`, `'options'`).
        * Type: String.

    * `http_username` / `http_password` / `http_auth_type`:

        * Optional. Auth credentials for HTTP(S) monitors. `http_auth_type` is `'basic'` or `'digest'`.
        * Type: String.

    * `post_type` / `post_value` / `post_content_type`:

        * Optional. Request body payload for `POST` / `PUT` / `PATCH` checks. `post_type` is `'key-value'` or `'raw data'`. `post_content_type` is `'text/html'` or `'content/json'`.
        * Type: String.

    * `custom_http_headers`:

        * Optional. Extra HTTP headers. Pass a JSON string or a dict.
        * Type: Dict / String.

    * `custom_http_statuses`:

        * Optional. Override which HTTP status codes count as up vs. down. UptimeRobot wire format applies (see UptimeRobot's documentation).
        * Type: String.

    * `ignore_ssl_errors`:

        * Optional. If `true`, accept invalid / self-signed TLS certificates.
        * Type: Bool.

    * `disable_domain_expire_notifications`:

        * Optional. `'disable'` silences UptimeRobot's domain-expiry warnings, `'enable'` keeps them on.
        * Type: String.

    * `alert_contacts`:

        * Optional. List of `{friendly_name | id, threshold, recurrence}` dicts referencing existing alert contacts. `threshold` is the alert delay in seconds (0 = immediately), `recurrence` is the re-alert interval in minutes (0 = no recurrence).
        * Type: List of dictionaries.

    * `mwindows`:

        * Optional. List of `{friendly_name | id}` dicts referencing existing maintenance windows.
        * Type: List of dictionaries.

    * `state`:

        * Optional. `'present'` (default) creates or updates the monitor; `'absent'` deletes it.
        * Type: String.

`uptimerobot__mwindows`

* List of maintenance windows to manage. The role synthesises each window's `friendly_name` as `'<type> [<value>] <start_time>-<end_time>'` (e.g. `weekly mon 03:30-05:30`). Pass `friendly_name` to override.
* Type: List of dictionaries.
* Default: `[]`

* Subkeys:

    * `type`:

        * Mandatory on create. Recurrence type: `'once'`, `'daily'`, `'weekly'`, `'monthly'`.
        * Type: String.

    * `value`:

        * For `type: 'weekly'`: day-of-week (`'mon'`..`'sun'`).
        * For `type: 'monthly'`: day-of-month (`'1'`..`'31'`).
        * Otherwise: unused.
        * Type: String.

    * `start_time`:

        * Mandatory on create. For `type: 'once'`: an RFC3339 timestamp. For `type: 'daily'` / `'weekly'` / `'monthly'`: `'HH:MM'`.
        * Type: String.

    * `end_time`:

        * Optional. `'HH:MM'`. Used together with `start_time` to compute `duration`. You can give either `end_time` or `duration`, not both.
        * Type: String.

    * `duration`:

        * Optional. Window duration in minutes.
        * Type: Number.

    * `status`:

        * Optional. `'active'` or `'paused'`. Only honoured on update.
        * Type: String.

    * `friendly_name`:

        * Optional. Overrides the synthesised name.
        * Type: String.

    * `state`:

        * Optional. `'present'` (default) or `'absent'`.
        * Type: String.

`uptimerobot__psps`

* List of public status pages to manage. Identified by `friendly_name`.
* Type: List of dictionaries.
* Default: `[]`

* Subkeys:

    * `friendly_name`:

        * Mandatory.
        * Type: String.

    * `monitors`:

        * Optional. List of `{friendly_name | id}` dicts referencing existing monitors. An empty / missing list publishes all monitors of the account.
        * Type: List of dictionaries.

    * `custom_domain` / `custom_url`:

        * Optional. Custom domain to host the status page (e.g. `'status.example.com'`). `custom_url` is an alias for compatibility with older inventories. Mutually exclusive.
        * Type: String.

    * `password`:

        * Optional. Password-protect the page.
        * Type: String.

    * `sort`:

        * Optional. Sort order of the listed monitors: `'a-z'`, `'z-a'`, `'up-down-paused'`, `'down-up-paused'`.
        * Type: String.

    * `hide_url_links`:

        * Optional. If `true`, the page does not show the underlying URLs.
        * Type: Bool.

    * `status`:

        * Optional. `'active'` or `'paused'`. Only honoured on update.
        * Type: String.

    * `state`:

        * Optional. `'present'` (default) or `'absent'`.
        * Type: String.

`uptimerobot__alert_contacts`

* Stale alert contacts to delete. UptimeRobot API v2 does not allow creating or editing alert contacts (web-UI only), so this list is delete-only. Each entry needs `state: 'absent'` plus either `id` or `friendly_name`.
* Type: List of dictionaries.
* Default: `[]`


## Example Inventory

A complete `group_vars/lfops_uptimerobot.yml` covering all four lists:

```yaml
uptimerobot__api_key: "{{ lookup('linuxfabrik.lfops.bitwarden_item', {
    'hostname': 'uptimerobot.com',
    'purpose': 'API key',
    'username': 'main',
    'collection_id': lfops__bitwarden_collection_id,
    'organization_id': lfops__bitwarden_organization_id,
  })['password'] }}"

uptimerobot__mwindows:
  - type: 'weekly'
    value: 'mon'
    start_time: '03:30'
    end_time: '05:30'
    status: 'active'
    state: 'present'
  - type: 'daily'
    start_time: '21:22'
    end_time: '21:32'
    status: 'active'
    state: 'present'

uptimerobot__monitors:
  - prefix: '001'
    url: 'https://www.example.com/index.php/login'
    interval: 120
    http_method: 'get'
    alert_contacts:
      - friendly_name: 'monitoring@example.com'
        threshold: 1
        recurrence: 0
    mwindows:
      - friendly_name: 'weekly mon 03:30-05:30'
    state: 'present'

  - prefix: '001'
    url: 'https://legacy.example.com'
    state: 'absent'

uptimerobot__psps:
  - friendly_name: 'Status - example.com'
    custom_url: 'status.example.com'
    monitors:
      - friendly_name: '001 www.example.com/index.php/login'
    sort: 'a-z'
    status: 'active'
    state: 'present'

uptimerobot__alert_contacts:
  - id: 7068316
    state: 'absent'
```


## Running the Role

The shipped playbook already targets `hosts: lfops_uptimerobot` internally, so put `localhost` (or wherever you keep your API key) into that group and run:

```bash
ansible-playbook --inventory path/to/inventory linuxfabrik.lfops.uptimerobot

# Only push maintenance windows:
ansible-playbook --inventory path/to/inventory linuxfabrik.lfops.uptimerobot --tags uptimerobot:mwindow

# Dry-run with per-resource diff output:
ansible-playbook --inventory path/to/inventory linuxfabrik.lfops.uptimerobot --check --diff
```

For ad-hoc / read-only queries against UptimeRobot, the modules can be invoked directly without the role:

```yaml
- name: 'Check UptimeRobot account quota'
  linuxfabrik.lfops.uptimerobot_account_info:
  register: ur_account
  delegate_to: 'localhost'

- name: 'Pause one monitor'
  linuxfabrik.lfops.uptimerobot_monitor:
    friendly_name: '001 maintenance-mode.example.com'
    status: 'paused'
    state: 'present'
  delegate_to: 'localhost'
```


## Performance / Caching

To keep the per-item API cost down when the role loops a CRUD module over a long list, `module_utils.uptimerobot` writes the four heavy `getX` responses (`getMonitors`, `getAlertContacts`, `getMWindows`, `getPSPs`) to a short-lived on-disk cache under `~/.cache/ansible-uptimerobot/` with a 60-second TTL. Cache files are mode `0600` because they hold the full resource list returned by the API.

* **Read calls** check the cache first; a hit replaces the (paginated) HTTP request entirely. Logged as `cache HIT <endpoint> (...)` in syslog.
* **Mutating calls** (`newX` / `editX` / `deleteX`) succeed against the API and then invalidate the matching `getX` cache so the next read sees the post-write state.
* Cache files are per-engineer (the path is in your `$HOME`), so different engineers running against the same UptimeRobot account don't share state.
* If you need to force a fresh read, delete the directory:

    ```
    rm -rf ~/.cache/ansible-uptimerobot/
    ```

Typical impact: a `--check` run over 56 monitors goes from ~56× 4 page `getMonitors` + 56× `getAlertContacts` + 56× `getMWindows` to one of each (the rest hit cache). Idempotent re-runs of the same playbook within a minute are nearly free.


## Debugging / Verbose Output

The CRUD modules emit verbose output through three channels — useful when iterating against a live API:

* **`module.log()`** lines go to syslog under the tag `ansible-linuxfabrik.lfops.uptimerobot_<resource>` (the full collection FQDN; that's the identifier Ansible uses when calling modules through a collection). They cover: API-key resolution source, lookup result (existing monitor / window / PSP found or not), every HTTP POST (endpoint plus sanitised key list — API key and passwords are masked), pagination page count, response status, diff field list.
* **`module.warn()`** is used on rate-limit retries (HTTP 429) so the playbook output shows how often the modules had to back off.
* The **`debug`** key in every module's return value carries a structured summary (`operation`, `friendly_name`, resource id, `diff_fields` or `sent_keys`).

### Tailing the syslog channel

The syslog tag is `ansible-linuxfabrik.lfops.uptimerobot_<resource>` (one tag per resource type). On a controller running systemd / journald:

```
# Live tail while a playbook runs:
journalctl --identifier ansible-linuxfabrik.lfops.uptimerobot_monitor --follow

# Everything from the last run, all UR resources at once:
journalctl --since '5 minutes ago' \
    --identifier ansible-linuxfabrik.lfops.uptimerobot_account_info \
    --identifier ansible-linuxfabrik.lfops.uptimerobot_alert_contact \
    --identifier ansible-linuxfabrik.lfops.uptimerobot_alert_contact_info \
    --identifier ansible-linuxfabrik.lfops.uptimerobot_monitor \
    --identifier ansible-linuxfabrik.lfops.uptimerobot_monitor_info \
    --identifier ansible-linuxfabrik.lfops.uptimerobot_mwindow \
    --identifier ansible-linuxfabrik.lfops.uptimerobot_mwindow_info \
    --identifier ansible-linuxfabrik.lfops.uptimerobot_psp \
    --identifier ansible-linuxfabrik.lfops.uptimerobot_psp_info
```

On a sysv / non-journald host, the same lines land in `/var/log/messages` (Red Hat-family) or `/var/log/syslog` (Debian-family). Filter with `grep ansible-uptimerobot_`.

The tag prefix is fixed in `module_utils/uptimerobot.py`; it does not change with `--verbose` and does not need any extra configuration on the controller.

### Reading the debug dict from the playbook side

Every CRUD and info module returns a `debug:` key alongside the resource payload. Capture it with `register:` and inspect it directly — much more compact than `-vvv`-level Ansible chatter:

```yaml
- linuxfabrik.lfops.uptimerobot_monitor:
    friendly_name: '001 www.example.com'
    url: 'https://www.example.com'
    type: 'http'
    interval: 30
    state: 'present'
  register: 'ur_result'

- ansible.builtin.debug:
    var: 'ur_result.debug'
```

Typical values you will see:

* `operation`: `'noop'`, `'create'`, `'create (check_mode)'`, `'update'`, `'update (check_mode)'`, `'delete'`, `'delete (check_mode)'`, `'list'`, `'read'`.
* `reason`: only set for `noop`, e.g. `'no diff'` or `'monitor not present'`.
* `friendly_name`, `monitor_id` / `mwindow_id` / `psp_id`: identifiers of the resource the module touched.
* `diff_fields`: list of field names that actually differ between current and desired state — what an `update` will send to the API, or what a `--check` `update (check_mode)` would send.
* `sent_keys`: list of field names included in a `create`'s body.
* `count`: number of items returned (info modules only).

Combined with `--check --diff`, the `debug` dict makes it cheap to investigate false-positive `changed: true` (typically a missing read-side translation or a desired-vs-current normalisation gap).


## Migrating from the `utr` CLI

Linuxfabrik used to drive the same configuration through the standalone `utr` CLI (`uptimerobot-cli`). Migration to this role is mechanical:

| `utr` file | Inventory variable |
|---|---|
| `utr.yml` (top-level `monitors:` list) | `uptimerobot__monitors` |
| `mwindows.yml` (top-level `mwindows:` list) | `uptimerobot__mwindows` |
| `psps.yml` (top-level `psps:` list) | `uptimerobot__psps` |
| `alertcontacts.yml` (top-level `alert_contacts:` list) | `uptimerobot__alert_contacts` |

The list items use the same field names — drop them into your inventory's `group_vars/lfops_uptimerobot.yml` (or wherever) and run the playbook. The auto-generated `friendly_name` follows the same `'<prefix> <url-without-protocol>'` (monitors) and `'<type> [<value>] <start_time>-<end_time>'` (mwindows) conventions, including the same prefix-collapse rule for URLs whose host already starts with the prefix (e.g. `prefix: '038'` plus URL `https://038-p-mon61…/icingaweb2/` becomes friendly_name `038-p-mon61…/icingaweb2/`).

Read-side parity with `utr get …` is provided by four read-only modules — useful for ad-hoc inspection, dynamic inventories, or driving downstream tasks:

| `utr` command | Ansible module |
|---|---|
| `utr get account` | `linuxfabrik.lfops.uptimerobot_account_info` |
| `utr get monitors` | `linuxfabrik.lfops.uptimerobot_monitor_info` |
| `utr get mwindows` | `linuxfabrik.lfops.uptimerobot_mwindow_info` |
| `utr get alert_contacts` | `linuxfabrik.lfops.uptimerobot_alert_contact_info` |
| `utr get psps` | `linuxfabrik.lfops.uptimerobot_psp_info` |

All info modules accept `friendly_name:` to filter to a single resource and (where supported by the API) `search:` for a server-side substring filter. Enum-style fields are returned as labels (e.g. `http_method: 'get'`, `status: 'up'`), matching the user-facing parameter values you write in your inventory.

```yaml
- linuxfabrik.lfops.uptimerobot_monitor_info:
    friendly_name: '001 www.example.com'
  register: ur_monitor

- ansible.builtin.debug:
    var: ur_monitor.monitors[0].interval
```

For the equivalent of `utr set monitors --status=paused`, loop the regular `uptimerobot_monitor` module with `state: 'present'` and `status: 'paused'` over the result of `uptimerobot_monitor_info`.


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
