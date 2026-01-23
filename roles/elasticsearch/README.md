# Ansible Role linuxfabrik.lfops.elasticsearch

This role installs and configures an Elasticsearch server.

Note that this role does NOT let you specify a particular Elasticsearch server version. It simply installs the latest available Elasticsearch server version from the repos configured in the system. If you want or need to install a specific version, have a look at the [linuxfabrik.lfops.repo_elasticsearch](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_elasticsearch) role.


## Mandatory Requirements

* Enable the official elasticsearch repository. This can be done using the [linuxfabrik.lfops.repo_elasticsearch](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_elasticsearch) role.

If you use the [elasticsearch playbook](https://github.com/Linuxfabrik/lfops/blob/main/playbooks/elasticsearch.yml), this is automatically done for you.


## Optional Requirements

* Set `vm.swappiness` to 1. This can be done using the [linuxfabrik.lfops.kernel_settings](https://github.com/Linuxfabrik/lfops/tree/main/roles/kernel_settings) role.

If you use the [elasticsearch playbook](https://github.com/Linuxfabrik/lfops/blob/main/playbooks/elasticsearch.yml), this is automatically done for you.


## Tags

| Tag                       | What it does                                   | Reload / Restart               |
| ---                       | ------------                                   | ----------------               |
| `elasticsearch`           | Installs and configures Elasticsearch          | Restarts elasticsearch.service |
| `elasticsearch:certs`     | Deploys TLS certificates                       | Restarts elasticsearch.service |
| `elasticsearch:configure` | Deploys configuration files                    | Restarts elasticsearch.service |
| `elasticsearch:state`     | Manages the state of the Elasticsearch service | -                              |


## Post-Installation Steps

After setting up a single node or cluster, generate the initial password for the `elastic` user:

```bash
/usr/share/elasticsearch/bin/elasticsearch-reset-password --username elastic
```


## Setting Up an Elasticsearch Cluster

This role supports creating a multi-node Elasticsearch cluster using manual certificate distribution. This approach provides full automation and avoids the limitations of Elasticsearch's enrollment token system (which requires interactive commands that cannot be automated in Ansible).

All cluster nodes must:
* Have the same `elasticsearch__cluster_name__*_var` configured
* Be able to communicate with each other (configure `elasticsearch__network_host` to be accessible from other nodes, e.g., `0.0.0.0` or a specific IP)
* Have `elasticsearch__discovery_seed_hosts` set to the list of all cluster nodes from the start


### Deploy First Node and Generate Certificates

Deploy Elasticsearch on the first node (stopped state) to use the certutil tool:
```bash
ansible-playbook --inventory inventory linuxfabrik.lfops.elasticsearch --limit node1.example.com --extra-vars='{"elasticsearch__service_state": "stopped"}'
```

Connect to the first node and generate certificates:
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

Copy the generated certificates to your Ansible inventory (have a look at the Optional Variables below for the paths).

The certificates are used for `elasticsearch__{http,transport}_{cert,key}`. It is possible to either use different certificates for http and transport or use the same for both.


### Bootstrap the First Node(s)

You can bootstrap one or more nodes - both options work. Starting with a single node makes troubleshooting easier. However, bear in mind that both the `master` and `data` roles are required for bootstrapping. Either the first node must have these roles, or multiple nodes must be bootstrapped.

```bash
ansible-playbook --inventory inventory linuxfabrik.lfops.elasticsearch --limit node1.example.com --extra-vars='{"elasticsearch__cluster_initial_master_nodes": ["node1.example.com"]}'
```

Attention: Only include the first node in `elasticsearch__cluster_initial_master_nodes`. If you include nodes that do not exist yet, the first node will wait indefinitely for them and the cluster will not form.


### Verify Cluster State

On the first node, generate the initial password and verify the cluster state:

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


### Deploy Additional Nodes

Note: Deploy remaining nodes without `elasticsearch__cluster_initial_master_nodes`.

```bash
ansible-playbook --inventory inventory linuxfabrik.lfops.elasticsearch --limit node2.example.com,node3.example.com
```
The nodes will automatically join the existing cluster using `elasticsearch__discovery_seed_hosts`.


### Clear Initial Master Nodes Configuration

After at least one additional master node has joined, remove the `cluster.initial_master_nodes` setting from the first node:

```bash
ansible-playbook --inventory inventory linuxfabrik.lfops.elasticsearch --limit node1.example.com --tags elasticsearch:configure
```
This prevents issues when the first node is restarted.


### Verify Complete Cluster

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

1. Generate certificates for the new node using the existing CA. On the node where the CA is stored:
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

2. Copy certificates to your inventory
3. Add the new node to `elasticsearch__discovery_seed_hosts` in group_vars
4. Create host_vars for the new node with a unique `elasticsearch__node_name`
5. Deploy the new node:

```bash
ansible-playbook --inventory inventory linuxfabrik.lfops.elasticsearch --limit new-node.example.com
```

6. Roll out the `elasticsearch__discovery_seed_hosts` to all cluster nodes


## Optional Role Variables

| Variable | Description | Default Value |
| -------- | ----------- | ------------- |
| `elasticsearch__action_auto_create_index__host_var` / <br> `elasticsearch__action_auto_create_index__group_var` | Automatic index creation allows any index to be created automatically. <br>For the usage in `host_vars` / `group_vars` (can only be used in one group at a time). | `true` |
| `elasticsearch__ca_cert` | ASCII-armored PEM CA certificate for TLS. When set, enables manual certificate management mode and disables auto-enrollment. All cluster nodes should use the same CA certificate. | unset |
| `elasticsearch__cluster_initial_master_nodes` | A list of initial master-eligible nodes. The entries have to match the `elasticsearch__node_name`. **IMPORTANT:** Only use this during initial cluster bootstrap via `--extra-vars`. Never set this permanently in inventory. After the first successful cluster start, all subsequent runs should omit this variable. | unset |
| `elasticsearch__cluster_name__host_var` / <br> `elasticsearch__cluster_name__group_var` | A descriptive name for your cluster. <br>For the usage in `host_vars` / `group_vars` (can only be used in one group at a time). | `'my-application'` |
| `elasticsearch__cluster_routing_allocation_awareness_attributes` | List of awareness attribute names to enable [shard allocation awareness](https://www.elastic.co/docs/deploy-manage/distributed-architecture/shard-allocation-relocation-recovery/shard-allocation-awareness). Distributes replicas across different attribute values to minimize risk of data loss during failures. Configure the same attributes on all master-eligible nodes | `[]` |
| `elasticsearch__cluster_routing_allocation_awareness_force` | Dictionary for forced awareness to prevent replica overloading when a location fails. Key is the attribute name, value is list of expected attribute values. Elasticsearch will leave replicas unassigned rather than concentrating them in remaining locations. | `{}` |
| `elasticsearch__discovery_seed_hosts` | A list of IPs or hostnames that point to all master-eligible nodes of the cluster. The port defaults to 9300 but can be overwritten using `:9301`, for example. | unset |
| `elasticsearch__http_cert` | ASCII-armored PEM HTTP certificate. | unset |
| `elasticsearch__http_key` | ASCII-armored PEM HTTP private key. | unset |
| `elasticsearch__network_host` | Sets the address for both HTTP and transport traffic. Accepts an IP address, a hostname, or a [special value](https://www.elastic.co/guide/en/elasticsearch/reference/8.19/modules-network.html#network-interface-values). | `'_local_'` |
| `elasticsearch__node_attributes` | Dictionary of custom node attributes. Can be used for shard allocation awareness. Each attribute identifies a node's physical location or characteristic. | `{}` |
| `elasticsearch__node_name` | A descriptive name for the node | `'{{ ansible_facts["nodename"] }}'` |
| `elasticsearch__node_roles` | List of roles for this node. Available roles: `master`, `data`, `data_content`, `data_hot`, `data_warm`, `data_cold`, `data_frozen`, `ingest`, `ml`, `remote_cluster_client`, `transform`, `voting_only`. See [Elasticsearch node roles documentation](https://www.elastic.co/guide/en/elasticsearch/reference/current/modules-node.html#node-roles). | unset |
| `elasticsearch__path_data` | Path to the directory where Elasticsearch stores its data. | `/var/lib/elasticsearch` |
| `elasticsearch__path_repos` | Paths pointing to [Shared file system repositories](https://www.elastic.co/docs/deploy-manage/tools/snapshot-and-restore/shared-file-system-repository) used for snapshots (backups). | `[]` |
| `elasticsearch__raw` | Multiline string. Raw content which will be appended to the `elasticsearch.yml` config file. | unset |
| `elasticsearch__service_enabled` | Enables or disables the elasticsearch service, analogous to `systemctl enable/disable --now`. | `true` |
| `elasticsearch__service_state` | Controls the state of the elasticsearch service, analogous to `systemctl start/stop/restart/reload`. Possible options:<br> * `started`<br> * `stopped`<br> * `restarted`<br> * `reloaded` | `'started'` |
| `elasticsearch__transport_cert` | ASCII-armored PEM transport certificate. | unset |
| `elasticsearch__transport_key` | ASCII-armored PEM transport private key. | unset |

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
elasticsearch__network_host: '0.0.0.0'
elasticsearch__network_host: '_local_'  # or '127.0.0.1' for single node
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
