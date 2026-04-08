# Ansible Role linuxfabrik.lfops.elasticsearch

This role installs and configures Elasticsearch, either as a single-node instance or as a multi-node cluster.

Note that this role does NOT let you specify a particular Elasticsearch server version. It simply installs the latest available Elasticsearch server version from the repos configured in the system. If you want or need to install a specific version, have a look at the [linuxfabrik.lfops.repo_elasticsearch](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_elasticsearch) role.


## Mandatory Requirements

* Enable the official Elasticsearch repository. This can be done using the [linuxfabrik.lfops.repo_elasticsearch](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_elasticsearch) role.

If you use the [elasticsearch playbook](https://github.com/Linuxfabrik/lfops/blob/main/playbooks/elasticsearch.yml), this is automatically done for you.


## Optional Requirements

* Set `vm.swappiness` to 1. This can be done using the [linuxfabrik.lfops.kernel_settings](https://github.com/Linuxfabrik/lfops/tree/main/roles/kernel_settings) role.

If you use the [elasticsearch playbook](https://github.com/Linuxfabrik/lfops/blob/main/playbooks/elasticsearch.yml), this is automatically done for you.


## Single-Node Setup

For a single-node setup, no special configuration is needed beyond the mandatory requirements. When `elasticsearch__discovery_seed_hosts` is not set, the role automatically configures `discovery.type: single-node`. After installation, generate the initial password for the `elastic` user (see Post-Installation Steps below).


## Tags

`elasticsearch`

* Installs Elasticsearch and unzip.
* Creates the data directory and tmp directory.
* Deploys all configuration files.
* Deploys TLS certificates (if `elasticsearch__ca_cert` is set).
* Manages the state of the Elasticsearch service.
* Triggers: elasticsearch.service restart.

`elasticsearch:certs`

* Deploys TLS certificates (CA, HTTP, transport).
* Triggers: elasticsearch.service restart.

`elasticsearch:configure`

* Deploys `/etc/elasticsearch/elasticsearch.yml`.
* Deploys `/etc/elasticsearch/log4j2.properties`.
* Deploys the sysconfig file.
* Deploys `/tmp/certutil.yml` (if `elasticsearch__discovery_seed_hosts` is set).
* Triggers: elasticsearch.service restart.

`elasticsearch:state`

* Manages the state of the Elasticsearch service (`systemctl enable/disable`, `start/stop/restart`).
* Triggers: none.


## Post-Installation Steps

After setting up a single node or cluster, generate the initial password for the `elastic` user:

```bash
/usr/share/elasticsearch/bin/elasticsearch-reset-password --username elastic
```


## Setting Up an Elasticsearch Cluster

This role supports creating a multi-node Elasticsearch cluster using manual certificate distribution. Elasticsearch 8.x ships with an enrollment token mechanism for adding nodes to a cluster. However, enrollment tokens expire after 30 minutes, and the process requires interactive commands on the command line. This makes it unsuitable for automation with Ansible. Instead, this role generates TLS certificates manually using `elasticsearch-certutil` and distributes them to all nodes via Ansible.

Note that a fully unattended cluster setup is not possible with Elasticsearch. The initial certificate generation and password creation require manual steps on the command line (see below). Once certificates exist, subsequent node deployments are fully automated. If you need a search engine with better automation support, consider [OpenSearch](https://github.com/Linuxfabrik/lfops/tree/main/roles/opensearch), where certificate generation and admin password setup are fully integrated into the Ansible role.

The following steps are marked as **manual** or **automated** accordingly.

All cluster nodes must:

* Have the same `elasticsearch__cluster_name__*_var` configured
* Be able to communicate with each other (configure `elasticsearch__network_host` to be accessible from other nodes, e.g., `0.0.0.0` or a specific IP)
* Have `elasticsearch__discovery_seed_hosts` set to the list of all cluster nodes from the start


### Deploy First Node and Generate Certificates (manual)

Deploy Elasticsearch on the first node (stopped state) to use the certutil tool (**automated**):
```bash
ansible-playbook --inventory inventory linuxfabrik.lfops.elasticsearch --limit node1.example.com --extra-vars='{"elasticsearch__service_state": "stopped"}'
```

Connect to the first node and generate certificates (**manual** - Elasticsearch does not provide a non-interactive way to do this):
```bash
# generate CA (use empty password for automation) with 10 years validity
# IMPORTANT: Back up this CA - it's needed for adding nodes later
/usr/share/elasticsearch/bin/elasticsearch-certutil ca --pem --out /etc/elasticsearch/ca.zip --days 3650
cd /etc/elasticsearch/
unzip ca.zip

# the role automatically creates /tmp/certutil.yml based on your inventory
# review and adjust the IPs/DNS names in /tmp/certutil.yml

# generate node certificates for all cluster nodes
/usr/share/elasticsearch/bin/elasticsearch-certutil cert \
  --ca-cert /etc/elasticsearch/ca/ca.crt \
  --ca-key /etc/elasticsearch/ca/ca.key \
  --in /tmp/certutil.yml \
  --pem \
  --out /tmp/certs.zip
```

Copy the generated certificates to your Ansible inventory (**manual**). Have a look at the Optional Variables below for the paths.

The certificates are used for `elasticsearch__{http,transport}_{cert,key}`. It is possible to either use different certificates for http and transport or use the same for both.


### Bootstrap the First Node(s) (automated)

You can bootstrap one or more nodes - both options work. Starting with a single node makes troubleshooting easier. However, bear in mind that both the `master` and `data` roles are required for bootstrapping. Either the first node must have these roles, or multiple nodes must be bootstrapped.

```bash
ansible-playbook --inventory inventory linuxfabrik.lfops.elasticsearch --limit node1.example.com --extra-vars='{"elasticsearch__cluster_initial_master_nodes": ["node1.example.com"]}'
```

Attention: Only include the first node in `elasticsearch__cluster_initial_master_nodes`. If you include nodes that do not exist yet, the first node will wait indefinitely for them and the cluster will not form.


### Verify Cluster State (manual)

On the first node, generate the initial password (**manual** - Elasticsearch requires this interactive command) and verify the cluster state:

```bash
/usr/share/elasticsearch/bin/elasticsearch-reset-password --username elastic

export ELASTIC_PASSWORD='your-password-here'
export elastic_host='node1.example.com'
export elastic_cacert='/etc/elasticsearch/certs/ca.crt'

# check cluster health (might be yellow with 1 node)
curl --cacert "$elastic_cacert" \
    --user "elastic:${ELASTIC_PASSWORD}" \
    --request GET "https://$elastic_host:9200/_cluster/health?pretty=true"

# list nodes (should show only node1)
curl --cacert "$elastic_cacert" \
    --user "elastic:${ELASTIC_PASSWORD}" \
    --request GET "https://$elastic_host:9200/_cat/nodes?v&h=name,ip,node.role"
```


### Deploy Additional Nodes (automated)

Deploy remaining nodes without `elasticsearch__cluster_initial_master_nodes`.

```bash
ansible-playbook --inventory inventory linuxfabrik.lfops.elasticsearch --limit node2.example.com,node3.example.com
```
The nodes will automatically join the existing cluster using `elasticsearch__discovery_seed_hosts`.


### Clear Initial Master Nodes Configuration (automated)

After at least one additional master node has joined, remove the `cluster.initial_master_nodes` setting from the first node:

```bash
ansible-playbook --inventory inventory linuxfabrik.lfops.elasticsearch --limit node1.example.com --tags elasticsearch:configure
```
This prevents issues when the first node is restarted.


### Verify Complete Cluster (manual)

Verify all nodes have joined the cluster:
```bash
curl --cacert "$elastic_cacert" \
    --user "elastic:${ELASTIC_PASSWORD}" \
    --request GET "https://$elastic_host:9200/_cluster/health?pretty=true"

curl --cacert "$elastic_cacert" \
    --user "elastic:${ELASTIC_PASSWORD}" \
    --request GET "https://$elastic_host:9200/_cat/nodes?v&h=name,ip,node.role"
```
The status should be `green` with all nodes listed.


## Adding a New Node to an Existing Cluster

1. Generate certificates for the new node using the existing CA (**manual**). On the node where the CA is stored:
```bash
cat > /tmp/new-node-cert.yml <<EOF
instances:
  - name: 'new-node.example.com'
    ip:
      - '127.0.0.1'
      - '192.0.2.1'
    dns:
      - 'localhost'
      - 'new-node.example.com' # make sure to always include the Common Name in the Subject Alternative Names as well
      - 'new-node'
EOF

/usr/share/elasticsearch/bin/elasticsearch-certutil cert \
  --ca-cert /etc/elasticsearch/ca/ca.crt \
  --ca-key /etc/elasticsearch/ca/ca.key \
  --in new-node-cert.yml \
  --pem \
  --out new-node-certs.zip
```

2. Copy certificates to your inventory (**manual**)
3. Add the new node to `elasticsearch__discovery_seed_hosts` in group_vars
4. Create host_vars for the new node with a unique `elasticsearch__node_name`
5. Deploy the new node (**automated**):

```bash
ansible-playbook --inventory inventory linuxfabrik.lfops.elasticsearch --limit new-node.example.com
```

6. Roll out the `elasticsearch__discovery_seed_hosts` to all cluster nodes (**automated**)


## Optional Role Variables

`elasticsearch__action_auto_create_index__host_var` / `elasticsearch__action_auto_create_index__group_var`

* Automatic index creation allows any index to be created automatically.
* For the usage in `host_vars` / `group_vars` (can only be used in one group at a time).
* Type: Boolean.
* Default: `true`

`elasticsearch__ca_cert`

* ASCII-armored PEM CA certificate for TLS. When set, enables manual certificate management mode and disables auto-enrollment. All cluster nodes should use the same CA certificate.
* Type: String.
* Default: unset

`elasticsearch__cluster_initial_master_nodes`

* A list of initial master-eligible nodes. The entries have to match the `elasticsearch__node_name`. Only use this during initial cluster bootstrap via `--extra-vars`. Never set this permanently in inventory. After the first successful cluster start, all subsequent runs should omit this variable.
* Type: List of strings.
* Default: unset

`elasticsearch__cluster_name__host_var` / `elasticsearch__cluster_name__group_var`

* A descriptive name for your cluster.
* For the usage in `host_vars` / `group_vars` (can only be used in one group at a time).
* Type: String.
* Default: `'my-application'`

`elasticsearch__cluster_routing_allocation_awareness_attributes`

* List of awareness attribute names to enable [shard allocation awareness](https://www.elastic.co/docs/deploy-manage/distributed-architecture/shard-allocation-relocation-recovery/shard-allocation-awareness). Distributes replicas across different attribute values to minimize risk of data loss during failures. Configure the same attributes on all master-eligible nodes.
* Type: List of strings.
* Default: `[]`

`elasticsearch__cluster_routing_allocation_awareness_force`

* Dictionary for forced awareness to prevent replica overloading when a location fails. Key is the attribute name, value is list of expected attribute values. Elasticsearch will leave replicas unassigned rather than concentrating them in remaining locations.
* Type: Dictionary.
* Default: `{}`

`elasticsearch__cluster_routing_allocation_disk_watermark_flood_stage`

* Flood stage percentage for [disk-based shard allocation](https://www.elastic.co/docs/reference/elasticsearch/configuration-reference/cluster-level-shard-allocation-routing-settings#disk-based-shard-allocation). Elasticsearch enforces a read-only index block on every index that has one or more shards allocated on nodes having at least one disk exceeding the flood stage.
* Type: Float (`0 <= n <= 1`).
* Default: `0.95`

`elasticsearch__cluster_routing_allocation_disk_watermark_high`

* High watermark percentage for [disk-based shard allocation](https://www.elastic.co/docs/reference/elasticsearch/configuration-reference/cluster-level-shard-allocation-routing-settings#disk-based-shard-allocation). Elasticsearch will not allocate shards to nodes whose disk usage exceeds this percentage.
* Type: Float (`0 <= n <= 1`).
* Default: `0.9`

`elasticsearch__cluster_routing_allocation_disk_watermark_low`

* Low watermark percentage for [disk-based shard allocation](https://www.elastic.co/docs/reference/elasticsearch/configuration-reference/cluster-level-shard-allocation-routing-settings#disk-based-shard-allocation). Elasticsearch will not allocate shards to nodes whose disk usage exceeds this percentage.
* Type: Float (`0 <= n <= 1`).
* Default: `0.85`

`elasticsearch__discovery_seed_hosts`

* A list of IPs or hostnames that point to all master-eligible nodes of the cluster. The port defaults to 9300 but can be overwritten using `:9301`, for example.
* Type: List of strings.
* Default: unset

`elasticsearch__http_cert`

* ASCII-armored PEM HTTP certificate.
* Type: String.
* Default: unset

`elasticsearch__http_key`

* ASCII-armored PEM HTTP private key.
* Type: String.
* Default: unset

`elasticsearch__log4j2_retention_days`

* Number of days to retain rotated Elasticsearch log files (server, deprecation, slowlog, audit). All log appenders rotate daily and delete files older than this value.
* Type: Number.
* Default: `3`

`elasticsearch__network_host`

* Sets the address for both HTTP and transport traffic. Accepts an IP address, a hostname, or a [special value](https://www.elastic.co/guide/en/elasticsearch/reference/8.19/modules-network.html#network-interface-values).
* Type: String.
* Default: `'_local_'`

`elasticsearch__node_attributes`

* Dictionary of custom node attributes. Can be used for shard allocation awareness. Each attribute identifies a node's physical location or characteristic.
* Type: Dictionary.
* Default: `{}`

`elasticsearch__node_name`

* A descriptive name for the node.
* Type: String.
* Default: `'{{ ansible_facts["nodename"] }}'`

`elasticsearch__node_roles`

* List of roles for this node. Available roles: `master`, `data`, `data_content`, `data_hot`, `data_warm`, `data_cold`, `data_frozen`, `ingest`, `ml`, `remote_cluster_client`, `transform`, `voting_only`. See [Elasticsearch node roles documentation](https://www.elastic.co/guide/en/elasticsearch/reference/current/modules-node.html#node-roles).
* Type: List of strings.
* Default: unset

`elasticsearch__path_data`

* Path to the directory where Elasticsearch stores its data.
* Type: String.
* Default: `'/var/lib/elasticsearch'`

`elasticsearch__path_repos`

* Paths pointing to [Shared file system repositories](https://www.elastic.co/docs/deploy-manage/tools/snapshot-and-restore/shared-file-system-repository) used for snapshots (backups).
* Type: List of strings.
* Default: `[]`

`elasticsearch__raw`

* Raw content which will be appended to the `elasticsearch.yml` config file.
* Type: Multiline string.
* Default: unset

`elasticsearch__service_enabled`

* Enables or disables the Elasticsearch service, analogous to `systemctl enable/disable --now`.
* Type: Boolean.
* Default: `true`

`elasticsearch__service_state`

* Controls the state of the Elasticsearch service, analogous to `systemctl start/stop/restart/reload`. Possible options: `started`, `stopped`, `restarted`, `reloaded`.
* Type: String.
* Default: `'started'`

`elasticsearch__transport_cert`

* ASCII-armored PEM transport certificate.
* Type: String.
* Default: unset

`elasticsearch__transport_key`

* ASCII-armored PEM transport private key.
* Type: String.
* Default: unset


Example:
```yaml
# optional
elasticsearch__action_auto_create_index__group_var: false
elasticsearch__ca_cert: '{{ lookup("ansible.builtin.file", "{{ inventory_dir }}/group_files/elasticsearch_cluster/etc/elasticsearch/certs/ca.crt") }}'
elasticsearch__cluster_name__group_var: 'my-cluster'
elasticsearch__cluster_name__host_var: 'my-single-node'
elasticsearch__cluster_routing_allocation_awareness_attributes:
  - 'datacenter'
elasticsearch__cluster_routing_allocation_awareness_force:
  datacenter:
    - 'dc1'
    - 'dc2'
    - 'dc3'
elasticsearch__discovery_seed_hosts:
  - 'node1.example.com'
  - 'node2.example.com'
  - 'node3.example.com:9301'
elasticsearch__http_cert: '{{ lookup("ansible.builtin.file", "{{ inventory_dir }}/host_files/{{ inventory_hostname }}/etc/elasticsearch/certs/http.crt") }}'
elasticsearch__http_key: '{{ lookup("ansible.builtin.file", "{{ inventory_dir }}/host_files/{{ inventory_hostname }}/etc/elasticsearch/certs/http.key") }}'
elasticsearch__log4j2_retention_days: 7
elasticsearch__network_host: '0.0.0.0'
elasticsearch__node_attributes:
  datacenter: 'dc1'
  host: 'pod01'
elasticsearch__node_name: 'node1'
elasticsearch__node_roles:
  - 'master'
  - 'remote_cluster_client'
elasticsearch__path_data: '/data'
elasticsearch__path_repos:
  - '/mnt/backups'
  - '/mnt/long_term_backups'
elasticsearch__raw: |-
  http.max_content_length: 200mb
  indices.recovery.max_bytes_per_sec: 100mb
elasticsearch__service_enabled: false
elasticsearch__service_state: 'stopped'
elasticsearch__transport_cert: '{{ lookup("ansible.builtin.file", "{{ inventory_dir }}/host_files/{{ inventory_hostname }}/etc/elasticsearch/certs/transport.crt") }}'
elasticsearch__transport_key: '{{ lookup("ansible.builtin.file", "{{ inventory_dir }}/host_files/{{ inventory_hostname }}/etc/elasticsearch/certs/transport.key") }}'
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
