# Ansible Role linuxfabrik.lfops.trend_micro

This role installs and activates the [Trend Vision One Endpoint Security](https://www.trendmicro.com/en_us/business/products/hybrid-cloud/vision-one-endpoint-security.html) agent (`v1es`) on Linux servers. It covers pre-flight checks, agent download and installation via the XBC API, agent registration, and Server & Workload Protection (SWP) activation.


*Available in the next LFOps release.*


## How the Role Behaves

Trend Vision One Endpoint Security combines two products on the same host, and this role configures both:

* Endpoint Sensor (XDR/EDR) is the Endpoint Basecamp agent (`tmxbc`). It is downloaded and installed through the XBC API.
* Server & Workload Protection (SWP) is the Deep Security agent (`ds_agent`). It ships inside the same full package and is activated against a Deep Security Manager (DSM).

The "Server & Workload Protection (SWP)" deployment script generated in the Vision One console contains every value the role needs. It bundles both products in one full package: it lists two scenario IDs (one for the Endpoint Sensor, one for SWP) and carries the SWP activation values. The role installs that package, waits for the SWP agent to come up, and then activates it against the DSM.


Further reading:

* Trend Micro concepts and products: https://docs.linuxfabrik.ch/software/trend-micro.html
* Agent platform compatibility: https://help.deepsecurity.trendmicro.com/20_0/on-premise/agent-compatibility.html


## Known Limitations

The role does not configure an HTTP/HTTPS proxy. On hosts that reach the Trend Micro backends only through a proxy, set the proxy globally on the target so both the installer download and `tmxbc` pick it up, for example in `/etc/environment`:
```bash
HTTP_PROXY=http://192.0.2.30:8080/
HTTPS_PROXY=http://192.0.2.30:8080/
http_proxy=http://192.0.2.30:8080/
https_proxy=http://192.0.2.30:8080/
```


## Requirements

* At least 2 GB of RAM. The Server & Workload Protection agent (`ds_agent`) enforces this minimum during its pre-check; on a host with less memory the pre-check fails and `ds_agent` is never installed.
* Running as `root` (use `become: true`).
* `/tmp` must be writable on the target host.

Supported architectures: `x86_64`, `aarch64`.

Manual steps:

* Generate the **Server & Workload Protection (SWP)** deployment script in the Vision One console and read the role variable values from it. This is mandatory: the script is the only source of the customer ID, company ID, scenario IDs and SWP activation values the role needs.
  **Use the SWP deployment script, not the Endpoint-Sensor-only one.** The Endpoint-Sensor-only script lists a single scenario ID and none of the SWP activation values (tenant ID, token, DSM FQDN), so the SWP agent (`ds_agent`) cannot be installed.

    1. In the Vision One console, make sure a "Server & Workload Protection" product instance exists. If not, create it under Service Management -> Create product instance -> Server & Workload Protection.
    2. Navigate to Endpoint Security -> Endpoint Inventory -> Agent Installer -> Deployment Script.
    3. Select "Server & Workload Protection" as the endpoint group and "Linux" as the operating system.
    4. The previewed script contains every value the role needs.

The script is a `bash` installer. Map its values to the role variables as follows (the script has separate `x86_64` and `aarch64` blocks; `company_id` is identical in both, only `scenario_ids` differ per architecture):

| Role variable                                    | Where it appears in the deployment script                                     |
| -------------                                    | -----------------------------------------                                     |
| `trend_micro__customer_id`                       | `CUSTOMER_ID="..."`                                                           |
| `trend_micro__group_id`                          | `GROUP_ID=...` (optional, defaults to `0`)                                    |
| `trend_micro__policy_id`                         | `POLICY_ID=...` (optional, defaults to `0`)                                   |
| `trend_micro__relay_group_id`                    | `RELAY_GROUP_ID=...` (optional, defaults to `0`)                              |
| `trend_micro__swp_dsm_fqdn`                      | the host in `dsa_control -a dsm://<host>:443/`                                |
| `trend_micro__swp_login.tenant_id`               | `tenantID:...` in the `dsa_control` activation line                           |
| `trend_micro__swp_login.token`                   | `token:...` in the `dsa_control` activation line                              |
| `trend_micro__xbc_env`                           | `XBC_ENV="..."` (optional, defaults to `prod-eu1`)                            |
| `trend_micro__xbc_fqdn`                          | `XBC_FQDN="..."`                                                              |
| `trend_micro__xbc_installer_company_id`          | `company_id` in the `HTTP_BODY` (identical in both `archType` blocks)         |
| `trend_micro__xbc_installer_<arch>_scenario_ids` | `scenario_ids` in the `HTTP_BODY` of the matching `archType` block (both IDs) |


## Tags

`trend_micro`

* Runs the pre-flight checks (supported architecture, scenario IDs, writable `/tmp`, minimum RAM).
* Installs the required packages (`curl`, `tar`).
* Downloads the installer from the XBC API and installs the Endpoint Sensor agent (`tmxbc`).
* Waits for agent registration.
* Activates Server & Workload Protection (`ds_agent`) against the Deep Security Manager.
* Triggers: none.


## Mandatory Role Variables

`trend_micro__customer_id`

* Customer ID used in the installer API request.
* Type: String.

`trend_micro__swp_dsm_fqdn`

* Deep Security Manager FQDN used to activate Server & Workload Protection.
* Type: String.

`trend_micro__swp_login`

* Server & Workload Protection activation credentials.
* Type: Dictionary.
* Subkeys:

    * `tenant_id`:

        * Mandatory. Tenant ID used to activate Server & Workload Protection.
        * Type: String.

    * `token`:

        * Mandatory. Activation token used to activate Server & Workload Protection.
        * Type: String.

`trend_micro__xbc_installer_aarch64_scenario_ids`

* List of scenario IDs for the aarch64 installer API request. Include all IDs from the deployment script (endpoint sensor and SWP). Required on aarch64 hosts only.
* Type: List of strings.

`trend_micro__xbc_installer_company_id`

* Company ID for the installer API request. The same value for both architectures.
* Type: String.

`trend_micro__xbc_installer_x86_64_scenario_ids`

* List of scenario IDs for the x86_64 installer API request. Include all IDs from the deployment script (endpoint sensor and SWP). Required on x86_64 hosts only.
* Type: List of strings.

Example:
```yaml
# mandatory
trend_micro__customer_id: 'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx'
trend_micro__swp_dsm_fqdn: 'agents.workload.de-1.cloudone.trendmicro.com'
trend_micro__swp_login:
  tenant_id: 'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx'
  token: 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
trend_micro__xbc_installer_aarch64_scenario_ids:
  - 'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx'
  - 'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx'
trend_micro__xbc_installer_company_id: 'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx'
trend_micro__xbc_installer_x86_64_scenario_ids:
  - 'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx'
  - 'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx'
```


## Optional Role Variables

`trend_micro__group_id`

* Agent group for organisation.
* Type: Number.
* Default: `0`

`trend_micro__policy_id`

* Security policy to apply. `0` means no specific policy.
* Type: Number.
* Default: `0`

`trend_micro__relay_group_id`

* Relay group for agent communication.
* Type: Number.
* Default: `0`

`trend_micro__xbc_env`

* XBC environment identifier.
* Type: String.
* Default: `'prod-eu1'`

`trend_micro__xbc_fqdn`

* XBC backend FQDN. Use the FQDN matching your region.
* Type: String.
* Default: `'api-eu1.xbc.trendmicro.com'`

Example:
```yaml
# optional
trend_micro__group_id: 10
trend_micro__policy_id: 42
trend_micro__relay_group_id: 5
trend_micro__xbc_fqdn: 'api-us1.xbc.trendmicro.com'
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
