# Ansible Role linuxfabrik.lfops.trend_micro

This role installs and activates the [Trend Vision One Endpoint Security](https://www.trendmicro.com/en_us/business/products/hybrid-cloud/vision-one-endpoint-security.html) agent (`v1es`) on Linux servers. It covers pre-flight checks, agent download and installation via the XBC API, agent registration, and Server & Workload Protection (SWP) activation.


*Available in the next LFOps release.*


## Background: Two Products, One Host

Trend Vision One Endpoint Security combines two products on the same host, and this role configures both:

* **Endpoint Sensor** (XDR/EDR) is the `tmxbc` / Endpoint Basecamp agent. It is downloaded and installed through the XBC API. It is configured via `customer_id`, the per-architecture `company_id` and `scenario_ids`, `xbc_fqdn`, and `xbc_env`.
* **Server & Workload Protection (SWP)** is the Deep Security agent (`ds_agent`). It ships inside the same full package and is activated against a Deep Security Manager (DSM). It is configured via `tenant_id`, `token`, `swp_dsm_fqdn`, and the optional `policy_id`, `group_id`, and `relay_group_id`.

The **Server & Workload Protection (SWP) deployment script** generated in the Vision One console contains every value the role needs. It bundles both products in one full package: it lists two scenario IDs (one for the Endpoint Sensor, one for SWP) and carries the SWP activation values. The role installs that package, waits for the SWP agent to come up, and then activates it against the DSM.

> **Use the SWP deployment script, not the Endpoint-Sensor-only one.** The Endpoint-Sensor-only script lists a single scenario ID and none of the SWP activation values (tenant ID, token, DSM FQDN), so the SWP agent (`ds_agent`) cannot be installed.


## Generating the Deployment Script

1. In the Vision One console, make sure a **Server & Workload Protection** product instance exists. If not, create it under **Service Management → Create product instance → Server & Workload Protection**.
2. Navigate to **Endpoint Security → Endpoint Inventory → Agent Installer → Deployment Script**.
3. Select **Server & Workload Protection** as the endpoint group and **Linux** as the operating system.
4. The previewed script contains every value the role needs.

The script is a `bash` installer. Map its values to the role variables as follows (the script has separate `x86_64` and `aarch64` blocks, so `company_id` and `scenario_ids` differ per architecture):

| Role variable | Where it appears in the deployment script |
| ------------- | ----------------------------------------- |
| `trend_micro__customer_id` | `CUSTOMER_ID="..."` |
| `trend_micro__group_id` | `GROUP_ID=...` (optional, defaults to `0`) |
| `trend_micro__policy_id` | `POLICY_ID=...` (optional, defaults to `0`) |
| `trend_micro__relay_group_id` | `RELAY_GROUP_ID=...` (optional, defaults to `0`) |
| `trend_micro__swp_dsm_fqdn` | the host in `dsa_control -a dsm://<host>:443/` |
| `trend_micro__swp_login.tenant_id` | `tenantID:...` in the `dsa_control` activation line |
| `trend_micro__swp_login.token` | `token:...` in the `dsa_control` activation line |
| `trend_micro__xbc_env` | `XBC_ENV="..."` (optional, defaults to `prod-eu1`) |
| `trend_micro__xbc_fqdn` | `XBC_FQDN="..."` |
| `trend_micro__xbc_installer_<arch>_company_id` | `company_id` in the `HTTP_BODY` of the matching `archType` block |
| `trend_micro__xbc_installer_<arch>_scenario_ids` | `scenario_ids` in the `HTTP_BODY` of the matching `archType` block (both IDs) |


## Relevant Information

Learn about Trend Micro Concepts and Products: https://docs.linuxfabrik.ch/software/trend-micro.html
Agent Platform Compability: https://help.deepsecurity.trendmicro.com/20_0/on-premise/agent-compatibility.html

## Mandatory Requirements

* At least 2 GB of RAM. The Server & Workload Protection agent (`ds_agent`) enforces this minimum during its pre-check; on a host with less memory the pre-check fails and `ds_agent` is never installed.
* Running as `root` (use `become: true`).
* `/tmp` must be writable on the target host.

Supported architectures: `x86_64`, `aarch64`.


## Tags

| Tag                    | What it does                                        | Reload / Restart |
| ---                    | ------------                                        | ---------------- |
| `trend_micro`          | Runs all tasks                                      | -                |
| `trend_micro:install`  | Installs `curl` and `tar` only                      | -                |


## Mandatory Role Variables

| Variable | Description |
| -------- | ----------- |
| `trend_micro__customer_id` | Customer ID used in the installer API request. Found in the Vision One deployment script preview. |
| `trend_micro__xbc_installer_x86_64_company_id` | Company ID for the x86\_64 installer API request. |
| `trend_micro__xbc_installer_x86_64_scenario_ids` | List of scenario IDs for the x86\_64 installer API request. Include all IDs from the deployment script (endpoint sensor and SWP).|
| `trend_micro__xbc_installer_aarch64_company_id` | Company ID for the aarch64 installer API request. |
| `trend_micro__xbc_installer_aarch64_scenario_ids` | List of scenario IDs for the aarch64 installer API request. Include all IDs from the deployment script (endpoint sensor and SWP).|
| `trend_micro__swp_dsm_fqdn` | Deep Security Manager FQDN used to activate Server & Workload Protection. |
| `trend_micro__swp_login` | Server & Workload Protection activation credentials. Dictionary with the keys `tenant_id` and `token`. Typically fed by `linuxfabrik.lfops.bitwarden_item`. |

Example:
```yaml
# mandatory
trend_micro__customer_id: 'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx'

trend_micro__xbc_installer_x86_64_company_id: 'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx'
trend_micro__xbc_installer_x86_64_scenario_ids:
  - '<scenario-id-1>'
  - '<scenario-id-2>'

trend_micro__xbc_installer_aarch64_company_id: 'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx'
trend_micro__xbc_installer_aarch64_scenario_ids:
  - '<scenario-id-3>'
  - '<scenario-id-4>'

trend_micro__swp_dsm_fqdn: 'agents.workload.de-1.cloudone.trendmicro.com'
trend_micro__swp_login:
  tenant_id: 'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx'
  token: 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
```


## Optional Role Variables

| Variable | Description | Default Value |
| -------- | ----------- | ------------- |
| `trend_micro__xbc_fqdn` | XBC backend FQDN. Use the FQDN matching your region. | `'api-eu1.xbc.trendmicro.com'` |
| `trend_micro__xbc_env` | XBC environment identifier. | `'prod-eu1'` |
| `trend_micro__policy_id` | Security policy to apply. `0` means no specific policy. | `0` |
| `trend_micro__group_id` | Agent group for organisation. | `0` |
| `trend_micro__relay_group_id` | Relay group for agent communication. | `0` |
| `trend_micro__proxy_addr` | Proxy hostname or IP. Leave empty for a direct connection. | `''` |
| `trend_micro__proxy_port` | Proxy port. | `''` |
| `trend_micro__proxy_login` | Proxy credentials. Dictionary with the keys `username` and `password`. Omit for a proxy that needs no authentication. | `{}` |
| `trend_micro__path_dsa` | Path to the `dsa_control` binary. | `'/opt/ds_agent/dsa_control'` |
| `trend_micro__path_identity_file` | Path polled to confirm agent registration. | `'/opt/TrendMicro/EndpointBasecamp/etc/.identity'` |

Example:
```yaml
# optional
trend_micro__xbc_fqdn: 'api-us1.xbc.trendmicro.com'
trend_micro__policy_id: 42
trend_micro__group_id: 10
trend_micro__relay_group_id: 5
trend_micro__proxy_addr: '192.0.2.30'
trend_micro__proxy_port: '8080'
trend_micro__proxy_login:
  username: 'proxyuser'
  password: 'linuxfabrik'
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
