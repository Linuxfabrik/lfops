# Ansible Role linuxfabrik.lfops.opensearch

This role installs and configures OpenSearch, either as a single-node instance or as a multi-node cluster.

Note that this role does NOT let you specify a particular OpenSearch version. It simply installs the latest available OpenSearch version from the repos configured in the system. If you want or need to install a specific version, use the `opensearch__version__host_var` / `opensearch__version__group_var` variables.

Supported versions:

* 1.x
* 2.x

Hints for configuring TLS:

* The admin certificate must not be the same as a node certificate. Using the same certificate results in: `Seems you use a node certificate. This is not permitted, you have to use a client certificate and register it as admin_dn in opensearch.yml`
* Node certificates must either have `extendedKeyUsage = serverAuth, clientAuth` (`TLS Web Server Authentication`, `TLS Web Client Authentication`, respectively) set, or no `Extended Key Usage` at all. Otherwise `securityadmin.sh` fails with: `ERR: An unexpected SSLHandshakeException occured: Received fatal alert: certificate_unknown`


## Mandatory Requirements

* Enable the official OpenSearch repository. This can be done using the [linuxfabrik.lfops.repo_opensearch](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_opensearch) role.

If you use the [opensearch playbook](https://github.com/Linuxfabrik/lfops/blob/main/playbooks/opensearch.yml), this is automatically done for you.


## Single-Node Setup

For a single-node setup, no special configuration is needed beyond the mandatory variables. When `opensearch__discovery_seed_hosts` is not set, OpenSearch 2.x automatically runs in single-node mode (`discovery.type: single-node`). After installation, verify that OpenSearch is running (see Post-Installation Steps below).


## Tags

`opensearch`

* Installs OpenSearch.
* Deploys all configuration files.
* Deploys TLS certificates and runs `securityadmin.sh` (if security plugin is enabled).
* Manages the state of the OpenSearch service.
* Triggers: opensearch.service restart.

`opensearch:configure`

* Deploys `/etc/opensearch/opensearch.yml`.
* Deploys `/etc/sysconfig/opensearch`.
* Deploys internal users configuration (if security plugin is enabled).
* Triggers: opensearch.service restart.

`opensearch:generate_certs`

* Generates self-signed TLS certificates on the Ansible controller using the SearchGuard TLS Tool.
* Triggers: none.

`opensearch:state`

* Manages the state of the OpenSearch service (`systemctl enable/disable --now`).
* Triggers: none.

`opensearch:user`

* Manages internal users (generates hashed passwords, deploys `internal_users.yml`).
* Triggers: opensearch.service restart, `securityadmin.sh`.


## Mandatory Role Variables

`opensearch__opensearch_initial_admin_password`

* For new installations of OpenSearch 2.12 and later, a custom admin password is required. Minimum 8 characters, must contain at least one uppercase letter, one lowercase letter, one digit, and one special character.
* Type: String.

Example:
```yaml
# mandatory
opensearch__opensearch_initial_admin_password: 'linuxfabrik'
```


## Post-Installation Steps

After setting up a single node or cluster, verify that OpenSearch is running:

```bash
curl 'https://localhost:9200' --user admin:your-password --insecure
```


## Setting Up an OpenSearch Cluster

This role supports creating a multi-node OpenSearch cluster using manual certificate distribution. TLS certificates are generated beforehand and distributed to all nodes via Ansible. The security plugin is configured with the certificate distinguished names of all cluster members.

All cluster nodes must:

* Have the same `opensearch__cluster_name__*_var` configured
* Be able to communicate with each other (configure `opensearch__network_host` accordingly, e.g., `0.0.0.0` or a specific IP)
* Have `opensearch__discovery_seed_hosts` set to the list of all cluster nodes from the start
* Have matching TLS certificates (same CA, correct node DNs)


### Generate TLS Certificates

You have two options:

**Option A: Use the built-in certificate generator (recommended for testing)**

This role includes a convenience feature to generate self-signed certificates using the [SearchGuard TLS Tool](https://docs.search-guard.com/latest/offline-tls-tool). The certificates are generated on the Ansible controller.

Configure the certificate generation variables:
```yaml
opensearch__generate_certs_admin_cn: 'OpenSearch Admin'
opensearch__generate_certs_base_dn: 'OU=Secure Services,O=ACME,ST=Zurich,C=CH'
opensearch__generate_certs_ca_cn: 'OpenSearch Self-signed RootCA'
opensearch__generate_certs_nodes:
  - cn: 'node1.example.com'
    ip: '192.0.2.10'
  - cn: 'node2.example.com'
    ip: '192.0.2.11'
  - cn: 'node3.example.com'
    ip: '192.0.2.12'
```

Run the certificate generation:
```bash
ansible-playbook --inventory inventory linuxfabrik.lfops.opensearch --tags opensearch:generate_certs
```

The generated certificates and the SearchGuard TLS Tool config are placed in `/tmp/opensearch-certs/`. Copy them to your Ansible inventory for deployment.

**Option B: Provide your own certificates**

Place your certificates in the inventory and reference them via the `opensearch__plugins_security_*` variables (see Optional Role Variables below).


### Bootstrap the First Node

Set the cluster variables in your inventory:

```yaml
# group_vars for the OpenSearch cluster group
opensearch__cluster_name__group_var: 'my-cluster'
opensearch__discovery_seed_hosts:
  - 'node1.example.com'
  - 'node2.example.com'
  - 'node3.example.com'
opensearch__network_host: '0.0.0.0'
opensearch__plugins_security_authcz_admin_dns:
  - 'CN=OpenSearch Admin,OU=Secure Services,O=ACME,ST=Zurich,C=CH'
opensearch__plugins_security_nodes_dns:
  - 'CN=node1.example.com,OU=Secure Services,O=ACME,ST=Zurich,C=CH'
  - 'CN=node2.example.com,OU=Secure Services,O=ACME,ST=Zurich,C=CH'
  - 'CN=node3.example.com,OU=Secure Services,O=ACME,ST=Zurich,C=CH'
# TLS certificates (example using file lookups)
opensearch__plugins_security_root_ca: '{{ lookup("ansible.builtin.file",
    "{{ inventory_dir }}/group_vars/my_opensearch_cluster_group/files/etc/opensearch/root-ca.pem")
  }}'
opensearch__plugins_security_admin_certificate: '{{ lookup("ansible.builtin.file",
    "{{ inventory_dir }}/group_vars/my_opensearch_cluster_group/files/etc/opensearch/admin.pem")
  }}'
opensearch__plugins_security_admin_certificate_key: '{{ lookup("ansible.builtin.file",
    "{{ inventory_dir }}/group_vars/my_opensearch_cluster_group/files/etc/opensearch/admin.key")
  }}'
opensearch__plugins_security_http_certificate: '{{ lookup("ansible.builtin.file",
    "{{ inventory_dir }}/host_vars/{{ inventory_hostname }}/files/etc/opensearch/node_http.pem")
  }}'
opensearch__plugins_security_http_certificate_key: '{{ lookup("ansible.builtin.file",
    "{{ inventory_dir }}/host_vars/{{ inventory_hostname }}/files/etc/opensearch/node_http.key")
  }}'
opensearch__plugins_security_transport_certificate: '{{ lookup("ansible.builtin.file",
    "{{ inventory_dir }}/host_vars/{{ inventory_hostname }}/files/etc/opensearch/node_transport.pem")
  }}'
opensearch__plugins_security_transport_certificate_key: '{{ lookup("ansible.builtin.file",
    "{{ inventory_dir }}/host_vars/{{ inventory_hostname }}/files/etc/opensearch/node_transport.key")
  }}'
```

Deploy the first node with `opensearch__cluster_initial_cluster_manager_nodes`:

```bash
ansible-playbook --inventory inventory linuxfabrik.lfops.opensearch \
  --limit node1.example.com \
  --extra-vars='{"opensearch__cluster_initial_cluster_manager_nodes": ["node1.example.com"]}'
```

**Important:** Only include the first node in `opensearch__cluster_initial_cluster_manager_nodes`. Including nodes that do not exist yet causes the first node to wait indefinitely and the cluster will not form.


### Verify Cluster State

```bash
curl 'https://node1.example.com:9200/_cluster/health?pretty' --user admin:your-password --insecure
curl 'https://node1.example.com:9200/_cat/nodes?v' --user admin:your-password --insecure
```


### Deploy Additional Nodes

Deploy remaining nodes without `opensearch__cluster_initial_cluster_manager_nodes`:

```bash
ansible-playbook --inventory inventory linuxfabrik.lfops.opensearch \
  --limit node2.example.com,node3.example.com
```

The nodes will automatically join the existing cluster using `opensearch__discovery_seed_hosts`.


### Clear Initial Cluster Manager Nodes Configuration

After all nodes have joined, remove the `cluster.initial_cluster_manager_nodes` setting from the first node:

```bash
ansible-playbook --inventory inventory linuxfabrik.lfops.opensearch \
  --limit node1.example.com \
  --tags opensearch:configure
```

This prevents issues when the first node is restarted later.


### Verify Complete Cluster

Verify all nodes have joined the cluster:
```bash
curl 'https://node1.example.com:9200/_cluster/health?pretty' --user admin:your-password --insecure
curl 'https://node1.example.com:9200/_cat/nodes?v' --user admin:your-password --insecure
```
The status should be `green` with all nodes listed.


## Adding a New Node to an Existing Cluster

1. Generate certificates for the new node using the same CA as the existing cluster.
2. Add the certificate files to your Ansible inventory.
3. Add the new node's DN to `opensearch__plugins_security_nodes_dns` in group_vars.
4. Add the new node to `opensearch__discovery_seed_hosts` in group_vars.
5. Create host_vars for the new node with a unique `opensearch__node_name`.
6. Deploy the new node:

```bash
ansible-playbook --inventory inventory linuxfabrik.lfops.opensearch --limit new-node.example.com
```

7. Roll out the updated `opensearch__discovery_seed_hosts` and `opensearch__plugins_security_nodes_dns` to all cluster nodes:

```bash
ansible-playbook --inventory inventory linuxfabrik.lfops.opensearch --tags opensearch:configure
```


## Optional Role Variables - General

Only optional if `opensearch__plugins_security_disabled` is `true`.

`opensearch__action_auto_create_index__host_var` / `opensearch__action_auto_create_index__group_var`

* Automatic index creation allows any index to be created automatically.
* For the usage in `host_vars` / `group_vars` (can only be used in one group at a time).
* Type: Bool.
* Default: `true`

`opensearch__cluster_name__host_var` / `opensearch__cluster_name__group_var`

* A descriptive name for your cluster.
* For the usage in `host_vars` / `group_vars` (can only be used in one group at a time).
* Type: String.
* Default: `'my-application'`

`opensearch__internal_users__host_var` / `opensearch__internal_users__group_var`

* Internal users that can access OpenSearch via HTTP Basic Auth.
* Type: List of dictionaries.
* Default: `[]`
* Subkeys:

    * `username`:

        * Mandatory. Username.
        * Type: String.

    * `password`:

        * Mandatory. Password.
        * Type: String.

    * `backend_roles`:

        * Optional. Backend roles.
        * Type: List of strings.
        * Default: `[]`

    * `state`:

        * Optional. State of the user. Either `present` or `absent`.
        * Type: String.
        * Default: `'present'`

`opensearch__network_host`

* Set the bind address to a specific IP.
* Type: String.
* Default: `'127.0.0.1'`

`opensearch__node_name`

* A descriptive name for the node.
* Type: String.
* Default: `'{{ ansible_facts["nodename"] }}'`

`opensearch__path_data__host_var` / `opensearch__path_data__group_var`

* Path to directory where to store the data. Directory will be created.
* For the usage in `host_vars` / `group_vars` (can only be used in one group at a time).
* Type: String.
* Default: `'/var/lib/opensearch'`

`opensearch__plugins_security_admin_certificate`

* The ASCII-armored public PEM admin certificate.
* Type: String.
* Default: unset

`opensearch__plugins_security_admin_certificate_key`

* The ASCII-armored private PEM admin key.
* Type: String.
* Default: unset

`opensearch__plugins_security_allow_unsafe_democertificates`

* When set to true, OpenSearch starts up with demo certificates. These certificates are issued only for demo purposes. See [security settings](https://opensearch.org/docs/latest/install-and-configure/configuring-opensearch/security-settings/#advanced-settings).
* Type: Bool.
* Default: `false`

`opensearch__plugins_security_authcz_admin_dns`

* List of distinguished names of certificates that should have admin permissions.
* Type: List of strings.
* Default: `[]`

`opensearch__plugins_security_disabled`

* Enables or disables the OpenSearch [security plugin](https://opensearch.org/docs/1.3/security-plugin/index/), which offers encryption, authentication, access control as well as audit logging and compliance.
* Type: Bool.
* Default: `false`

`opensearch__plugins_security_http_certificate`

* The ASCII-armored public PEM HTTP certificate.
* Type: String.
* Default: unset

`opensearch__plugins_security_http_certificate_key`

* The ASCII-armored private PEM HTTP key.
* Type: String.
* Default: unset

`opensearch__plugins_security_root_ca`

* The ASCII-armored public PEM root CA certificate.
* Type: String.
* Default: unset

`opensearch__plugins_security_transport_certificate`

* The ASCII-armored public PEM transport certificate.
* Type: String.
* Default: unset

`opensearch__plugins_security_transport_certificate_key`

* The ASCII-armored private PEM transport key.
* Type: String.
* Default: unset

`opensearch__plugins_security_transport_enforce_hostname_verification`

* See [hostname verification](https://opensearch.org/docs/latest/security/configuration/tls/#advanced-hostname-verification-and-dns-lookup).
* Type: Bool.
* Default: `true`

`opensearch__plugins_security_transport_resolve_hostname`

* See [hostname verification](https://opensearch.org/docs/latest/security/configuration/tls/#advanced-hostname-verification-and-dns-lookup).
* Type: Bool.
* Default: `true`

`opensearch__service_enabled`

* Enables or disables the OpenSearch service, analogous to `systemctl enable/disable --now`.
* Type: Bool.
* Default: `true`

`opensearch__version__host_var` / `opensearch__version__group_var`

* The version of OpenSearch to install. If unset, the latest version will be installed. Note that the version format is OS-dependent: use `-2.15.0` on RHEL and `=2.15.0*` on Debian.
* For the usage in `host_vars` / `group_vars` (can only be used in one group at a time).
* Type: String.
* Default: unset

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
  - 'CN=OpenSearch Admin,OU=Secure Services,O=ACME,ST=Zurich,C=CH'
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
opensearch__version__host_var: '-2.15.0' # rhel
opensearch__version__host_var: '=2.15.0*' # debian
```


## Optional Role Variables - Cluster Configuration

`opensearch__cluster_initial_cluster_manager_nodes`

* A list of initial master-eligible nodes. The entries have to match the `opensearch__node_name`. Only use this during initial cluster bootstrap via `--extra-vars`. Never set this permanently in inventory. After the first successful cluster start, all subsequent runs should omit this variable.
* Type: List of strings.
* Default: unset

`opensearch__discovery_seed_hosts`

* A list of IPs or hostnames that point to all master-eligible nodes of the cluster. The port defaults to 9300 but can be overwritten by appending it to the hostname.
* Type: List of strings.
* Default: unset

`opensearch__plugins_security_nodes_dns`

* List of distinguished names of all cluster member certificates.
* Type: List of strings.
* Default: `[]`

Example:
```yaml
# cluster configuration
opensearch__discovery_seed_hosts:
  - 'node1.example.com'
  - 'node2.example.com'
  - 'node3.example.com:9301'
opensearch__plugins_security_nodes_dns:
  - 'CN=node1.example.com,OU=Secure Services,O=ACME,ST=Zurich,C=CH'
  - 'CN=node2.example.com,OU=Secure Services,O=ACME,ST=Zurich,C=CH'
  - 'CN=node3.example.com,OU=Secure Services,O=ACME,ST=Zurich,C=CH'
```


## TLS Certificate Generation Variables

These variables are only needed when using the built-in certificate generator (see "Setting Up an OpenSearch Cluster" above). The tasks run against the Ansible controller. Internally, the [SearchGuard TLS Tool](https://docs.search-guard.com/latest/offline-tls-tool) is used, with the generated config at `/tmp/opensearch-certs/config/{{ inventory_hostname }}-tlsconfig.yml`.

`opensearch__generate_certs_admin_cn`

* The common name of the admin certificate.
* Type: String.
* Default: `'OpenSearch Admin'`

`opensearch__generate_certs_base_dn`

* The base distinguished name for all the self-signed certificates.
* Type: String.
* Default: `'OU=Secure Services,O=ACME,ST=Zurich,C=CH'`

`opensearch__generate_certs_ca_cn`

* The common name of the CA certificate.
* Type: String.
* Default: `'OpenSearch Self-signed RootCA'`

`opensearch__generate_certs_nodes`

* List of dictionaries for the node certificates.
* Type: List of dictionaries.
* Default: `[]`
* Subkeys:

    * `cn`:

        * Mandatory. Common name of the node certificate.
        * Type: String.

    * `ip`:

        * Mandatory. IP address of the node.
        * Type: String.

Example:
```yaml
# tls certificate generation
opensearch__generate_certs_admin_cn: 'OpenSearch Admin'
opensearch__generate_certs_base_dn: 'OU=Secure Services,O=ACME,ST=Zurich,C=CH'
opensearch__generate_certs_ca_cn: 'OpenSearch Self-signed RootCA'
opensearch__generate_certs_nodes:
  - cn: 'node1.example.com'
    ip: '192.0.2.10'
  - cn: 'node2.example.com'
    ip: '192.0.2.11'
  - cn: 'node3.example.com'
    ip: '192.0.2.12'
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
