# Ansible Role linuxfabrik.lfops.trend_micro

This role installs and activates the [TrendAI Vision One Endpoint Security](https://www.trendmicro.com/en_us/business/products/hybrid-cloud/vision-one-endpoint-security.html) agent (`v1es`) on Linux servers. It covers pre-flight checks, agent download and installation via the XBC API, agent registration, and Server & Workload Protection (SWP) activation.

To find the installer IDs needed to configure this role:
1. Navigate to **Vision One → Endpoint Security → Endpoint Inventory → Agent Installer → Deployment Script**.
2. Select **Endpoint Sensor** as the protection type and **Linux** as the operating system.
3. The script preview contains the `company_id` and both scenario IDs.

To find the values needed for SWP activation:
1. Navigate to **Vision One → Endpoint Security → Server & Workload Protection → Adminstration → Local → Generate Deployment Scripts**.
2. Click **Generate Deployment Scripts**
3. After selecting your environment, the script that is being previewed, provides: tenantID, token, policyid, relaygroupid, groupid, DSM FQDN

For both of these workflows, you might need to create a product under the Service Management tab if you do not already have that.
For the agent download and the installation via the XBC API, you need to select **Create product instance** →  then select **Instance Type Standard Endpoint Protection**
To configure SWP you need to select **Create product instance** → then select **Server & Workload Protection**


## Relevant Information

Learn about Trend Micro Concepts and Products: https://docs.linuxfabrik.ch/software/trend-micro.html
Agent Platform Compability: https://help.deepsecurity.trendmicro.com/20_0/on-premise/agent-compatibility.html

## Mandatory Requirements

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
| `trend_micro__xbc_fqdn` | XBC backend FQDN. Use the FQDN matching your region (e.g. `api-eu1.xbc.trendmicro.com`). |
| `trend_micro__xbc_agent_token_x86_64` | Pipe-separated scenario IDs for the x86\_64 agent (e.g. `<id1>\|<id2>`). |
| `trend_micro__xbc_installer_x86_64_company_id` | Company ID for the x86\_64 installer API request. |
| `trend_micro__xbc_installer_x86_64_scenario_ids` | List of scenario IDs for the x86\_64 installer API request. |
| `trend_micro__xbc_agent_token_aarch64` | Pipe-separated scenario IDs for the aarch64 agent. |
| `trend_micro__xbc_installer_aarch64_company_id` | Company ID for the aarch64 installer API request. |
| `trend_micro__xbc_installer_aarch64_scenario_ids` | List of scenario IDs for the aarch64 installer API request. |
| `trend_micro__swp_dsm_fqdn` | Deep Security Manager FQDN used to activate Server & Workload Protection. |
| `trend_micro__tenant_id` | Tenant ID for SWP activation. |
| `trend_micro__token` | Token for SWP activation. |

Example:
```yaml
# mandatory
trend_micro__customer_id: 'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx'
trend_micro__xbc_fqdn: 'api-eu1.xbc.trendmicro.com'

trend_micro__xbc_agent_token_x86_64: '<scenario-id-1>|<scenario-id-2>'
trend_micro__xbc_installer_x86_64_company_id: 'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx'
trend_micro__xbc_installer_x86_64_scenario_ids:
  - '<scenario-id-1>'
  - '<scenario-id-2>'

trend_micro__xbc_agent_token_aarch64: '<scenario-id-3>|<scenario-id-4>'
trend_micro__xbc_installer_aarch64_company_id: 'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx'
trend_micro__xbc_installer_aarch64_scenario_ids:
  - '<scenario-id-3>'
  - '<scenario-id-4>'

trend_micro__swp_dsm_fqdn: 'agents.workload.de-1.cloudone.trendmicro.com'
trend_micro__tenant_id: 'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx'
trend_micro__token: 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
```


## Optional Role Variables

| Variable | Description | Default Value |
| -------- | ----------- | ------------- |
| `trend_micro__xbc_env` | XBC environment identifier. | `'prod-eu1'` |
| `trend_micro__policy_id` | Security policy to apply. `0` means no specific policy. | `0` |
| `trend_micro__group_id` | Agent group for organisation. | `0` |
| `trend_micro__relay_group_id` | Relay group for agent communication. | `0` |
| `trend_micro__proxy_addr` | Proxy hostname or IP. Leave empty for a direct connection. | `''` |
| `trend_micro__proxy_port` | Proxy port. | `''` |
| `trend_micro__proxy_username` | Proxy username. Omit if not required. | `''` |
| `trend_micro__proxy_password` | Proxy password. Omit if not required. | `''` |
| `trend_micro__path_dsa` | Path to the `dsa_control` binary. | `'/opt/ds_agent/dsa_control'` |
| `trend_micro__path_identity_file` | Path polled to confirm agent registration. | `'/opt/TrendMicro/EndpointBasecamp/etc/.identity'` |
| `trend_micro__install_log` | Installation log path on the target host. | `'/tmp/v1es_install.log'` |

Example:
```yaml
# optional
trend_micro__policy_id: 42
trend_micro__group_id: 10
trend_micro__relay_group_id: 5
trend_micro__proxy_addr: '172.30.1.30'
trend_micro__proxy_port: '8080'
trend_micro__proxy_username: 'proxyuser'
trend_micro__proxy_password: 'proxypass'
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
