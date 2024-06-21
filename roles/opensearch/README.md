# Ansible Role linuxfabrik.lfops.opensearch

This role installs and configures a OpenSearch server. Optionally, it allows the creation of a cluster setup.

TODO:
* This role needs to be adapted to the latest https://opensearch.org/docs/latest/install-and-configure/install-opensearch/rpm/ and https://opensearch.org/docs/latest/install-and-configure/install-opensearch/debian/ documents.
* Currently this role does not follow the configuration hints on https://opensearch.org/docs/latest/install-and-configure/install-opensearch/index/.

Hints for configuring TLS:
* The admin certificate cannot be the same as the node certificate. This will lead to the following error: `Seems you use a node certificate. This is not permitted, you have to use a client certificate and register it as admin_dn in opensearch.yml`
* The node certificates either need to have `extendedKeyUsage = serverAuth, clientAuth` (`TLS Web Server Authentication`, `TLS Web Client Authentication`, respectively) set, or no `Extended Key Usage` at all. Else running `securityadmin.sh` results in `ERR: An unexpected SSLHandshakeException occured: Received fatal alert: certificate_unknown`.

Currently supported versions:
* 1.x
* 2.x


## Mandatory Requirements

* Enable the official OpenSearch repository. This can be done using the [linuxfabrik.lfops.repo_opensearch](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_opensearch) role.

If you use the [opensearch playbook](https://github.com/Linuxfabrik/lfops/blob/main/playbooks/opensearch.yml), this is automatically done for you.


## Tags

| Tag             | What it does                            |
| ---             | ------------                            |
| `opensearch`       | <ul><li>Install opensearch-`{{ opensearch__version__combined_var }}`</li><li>Deploy `/etc/opensearch/opensearch.yml`</li><li>Deploy `/etc/sysconfig/opensearch`</li><li>`systemctl {{ opensearch__service_enabled \| bool \| ternary("enable", "disable") }} --now opensearch.service`</li></ul> |
| `opensearch:state` | <ul><li>`systemctl {{ opensearch__service_enabled \| bool \| ternary("enable", "disable") }} --now opensearch.service`</li></ul> |
| `opensearch:configure` | Deploys the config files and configures the security plugin |


## Optional Role Variables - General

| Variable | Description | Default Value |
| -------- | ----------- | ------------- |
| `opensearch__action_auto_create_index__host_var` / <br> `opensearch__action_auto_create_index__group_var` | Automatic index creation allows any index to be created automatically.  <br>For the usage in `host_vars` / `group_vars` (can only be used in one group at a time). | `true` |
| `opensearch__cluster_name__host_var` / <br> `opensearch__cluster_name__group_var` | A descriptive name for your cluster.  <br>For the usage in `host_vars` / `group_vars` (can only be used in one group at a time). | `'my-application'` |
| `opensearch__internal_users__host_var` / <br> `opensearch__internal_users__group_var` | List of dictionaries. Internal users that can access OpenSearch via HTTP Basic Auth. Subkeys: <ul><li>`username`: Mandatory, string. Username.</li><li>`password`: Mandatory, string. Password.</li><li>`backend_roles`: Optional, list. Defaults to `[]`.</li><li>`state`: Optional, string. State of the user. Either `present` or `absent`.</li></ul> |
| `opensearch__network_host` | Set the bind address to a specific IP. | `'127.0.0.1'` |
| `opensearch__node_name` | A descriptive name for the node | `'{{ ansible_facts["nodename"] }}'` |
| `opensearch__path_data__host_var` / <br> `opensearch__path_data__group_var` | Path to directory where to store the data. Directory will be created. | `'/var/lib/opensearch'` |
| `opensearch__plugins_security_admin_certificate` | The ASCII-armored public PEM admin certificate. | unset |
| `opensearch__plugins_security_admin_certificate_key` | The ASCII-armored private PEM admin key. | unset |
| `opensearch__plugins_security_allow_unsafe_democertificates` | When set to true, OpenSearch starts up with demo certificates. These certificates are issued only for demo purposes. See https://opensearch.org/docs/latest/install-and-configure/configuring-opensearch/security-settings/#advanced-settings | `false` |
| `opensearch__plugins_security_authcz_admin_dns` | List of distinguished names of certificates that should have admin permissions. | `[]` |
| `opensearch__plugins_security_disabled` | Enables or disables the opensearch [security plugin](https://opensearch.org/docs/1.3/security-plugin/index/), which offers encryption, authentication, access control as well as audit logging and compliance. | `false` |
| `opensearch__plugins_security_http_certificate` | The ASCII-armored public PEM http certificate. | unset |
| `opensearch__plugins_security_http_certificate_key` | The ASCII-armored private PEM http key. | unset |
| `opensearch__plugins_security_root_ca` | The ASCII-armored public PEM root CA certificate. | unset |
| `opensearch__plugins_security_transport_certificate` | The ASCII-armored public PEM transport certificate. | unset |
| `opensearch__plugins_security_transport_certificate_key` | The ASCII-armored private PEM transport key. | unset |
| `opensearch__plugins_security_transport_enforce_hostname_verification` | See https://opensearch.org/docs/latest/security/configuration/tls/#advanced-hostname-verification-and-dns-lookup | `false` |
| `opensearch__plugins_security_transport_resolve_hostname` | See https://opensearch.org/docs/latest/security/configuration/tls/#advanced-hostname-verification-and-dns-lookup | `true` |
| `opensearch__service_enabled` | Enables or disables the opensearch service, analogous to `systemctl enable/disable --now`. | `true` |
| `opensearch__version__host_var` / <br> `opensearch__version__group_var` | The version of OpenSearch which should be installed. If unset, latest will be installed.  <br>For the usage in `host_vars` / `group_vars` (can only be used in one group at a time). | unset |

Example:
```yaml
# optional
opensearch__action_auto_create_index__host_var: false
opensearch__cluster_name__host_var: 'my-cluster'
opensearch__internal_users__host_var:
  - username: 'opensearch-admin'
    password: 'linuxfabrik'
    backend_roles:
      - 'admin'
opensearch__network_host: '127.0.0.1'
opensearch__node_name: 'my-node1'
opensearch__path_data__host_var: '/var/lib/opensearch'
opensearch__plugins_security_admin_certificate: '{{ lookup("ansible.builtin.file",
    "{{ inventory_dir }}/group_vars/my_opensearch_cluster_group/files/etc/opensearch/admin.pem")
  }}'
opensearch__plugins_security_admin_certificate_key: '{{ lookup("ansible.builtin.file",
    "{{ inventory_dir }}/group_vars/my_opensearch_cluster_group/files/etc/opensearch/admin.key")
  }}'
opensearch__plugins_security_allow_unsafe_democertificates: false
opensearch__plugins_security_authcz_admin_dns:
  - 'CN=A,OU=UNIT,O=ORG,L=TORONTO,ST=ONTARIO,C=CA'
opensearch__plugins_security_disabled: false
opensearch__plugins_security_http_certificate: '{{ lookup("ansible.builtin.file",
    "{{ inventory_dir }}/host_vars/{{ inventory_hostname }}/files/etc/opensearch/node_http.pem")
  }}'
opensearch__plugins_security_http_certificate_key: '{{ lookup("ansible.builtin.file",
    "{{ inventory_dir }}/host_vars/{{ inventory_hostname }}/files/etc/opensearch/node_http.key")
  }}'
opensearch__plugins_security_root_ca: '{{ lookup("ansible.builtin.file",
    "{{ inventory_dir }}/group_vars/my_opensearch_cluster_group/files/etc/opensearch/root-ca.pem")
  }}'
opensearch__plugins_security_transport_certificate: '{{ lookup("ansible.builtin.file",
    "{{ inventory_dir }}/host_vars/{{ inventory_hostname }}/files/etc/opensearch/node_transport.pem")
  }}'
opensearch__plugins_security_transport_certificate_key: '{{ lookup("ansible.builtin.file",
    "{{ inventory_dir }}/host_vars/{{ inventory_hostname }}/files/etc/opensearch/node_transport.key")
  }}'
opensearch__plugins_security_transport_enforce_hostname_verification: false
opensearch__plugins_security_transport_resolve_hostname: true
opensearch__service_enabled: false
opensearch__version__host_var: '2.5.0'
```

## Optional Role Variables - TLS Certificate Generation

Use the following variables to easily generate self-signed certificates. These tasks run against the ansible controller. Internally, the [SecureGuard TLS Tool](https://docs.search-guard.com/latest/offline-tls-tool) is used for this, with the generated config at `/tmp/opensearch-certs/config/{{ inventory_hostname }}-tlsconfig.yml`.

| Variable | Description | Default Value |
| -------- | ----------- | ------------- |
| `opensearch__generate_certs_admin_cn` | The common name of the admin certificate. | `'OpenSearch Admin'` |
| `opensearch__generate_certs_base_dn` | The base distinguished name for all the self-signed certificates. | `'OU=Secure Services,O=ACME,ST=Zurich,C=CH'` |
| `opensearch__generate_certs_ca_cn` | The common name of the CA certificate. | `'OpenSearch Self-signed RootCA'` |
| `opensearch__generate_certs_nodes` | List of dictionaries for the node certificates. Subkeys: <ul><li>`cn`: Mandatory, string. Common name of the node certificate.</li><li>`ip`: Mandatory, string. IP address of the node.</li></ul> | `[]` |

Example:
```yaml
# tls certificate generation
opensearch__generate_certs_admin_cn: 'OpenSearch Admin'
opensearch__generate_certs_base_dn: 'OU=Secure Services,O=ACME,ST=Zurich,C=CH'
opensearch__generate_certs_ca_cn: 'OpenSearch Self-signed RootCA'
opensearch__generate_certs_nodes:
  - cn: 'node1.example.com'
    ip: '192.0.2.10'
```

## Optional Role Variables - Cluster Configuration

Use the following variables if you want to setup a OpenSearch cluster. Make sure that the cluster members can reach each other by setting `opensearch__network_host` accordingly.

You can check the status of the cluster with the following commands:
```bash
curl 'https://localhost:9200/_cluster/health?pretty' --user opensearch-admin:linuxfabrik --insecure
curl 'https://localhost:9200/_cat/nodes?v' --user opensearch-admin:linuxfabrik --insecure
```

| Variable | Description | Default Value |
| -------- | ----------- | ------------- |
| `opensearch__cluster_initial_cluster_manager_nodes` | A list of initial master-eligible nodes. The entries have to match the `opensearch__node_name`. You need to set this once when bootstrapping the cluster (aka the first start of the cluster). Make sure to remove this option after the first start, the nodes should not restart with this option active. Most of the time contains the same value as `opensearch__discovery_seed_hosts`. | unset |
| `opensearch__discovery_seed_hosts` | A list of IPs or hostnames that point to other master-eligible nodes of the cluster. The port defaults to 9300 but can be overwritten using `:9301`, for example. | unset |
| `opensearch__plugins_security_nodes_dns` | List of distinguished names of the other cluster members. | `[]` |

Example:
```yaml
# cluster configuration
opensearch__cluster_initial_cluster_manager_nodes:
  - 'node1.example.com'
  - 'node2.example.com'
  - 'node3.example.com'
opensearch__discovery_seed_hosts:
  - 'node1.example.com'
  - 'node2.example.com'
  - 'node3.example.com'
opensearch__plugins_security_nodes_dns:
  - 'CN=node1.example.com,OU=ops,O=acme,L=Zuerich,ST=Zuerich,C=CH'
  - 'CN=node2.example.com,OU=ops,O=acme,L=Zuerich,ST=Zuerich,C=CH'
  - 'CN=node3.example.com,OU=ops,O=acme,L=Zuerich,ST=Zuerich,C=CH'
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
