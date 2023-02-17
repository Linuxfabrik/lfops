# Ansible Role linuxfabrik.lfops.minio_client

This role installs the MinIO client binary, including bash completion and sets config location to `/etc/mc/`.

Runs on

* Rocky 8


## Tags

| Tag            | What it does                         |
| ---            | ------------                         |
| `minio_client` | Installs and configures MinIO client |
| `minio_client` | Configures MinIO client              |


## Optional Role Variables

| Variable | Description | Default Value |
| -------- | ----------- | ------------- |
| `minio_client__aliases__group_var` /<br> `minio_client__aliases__host_var` | List of MinIO connection aliases. Subkeys: <ul><li>`name`: Mandatory, string. Name of the alias. Has to be unique.</li><li>`access_key`: Mandatory, string. The S3 and Elastic Compute Cloud (EC2) Access Key.</li><li>`secret_key`: Mandatory, string. The S3 and Elastic Compute Cloud (EC2) Secret Key.</li><li>`api`: Optional, string. The API signature. Possible options: `'S3v4'` or `'S3v2'`. Defaults to `'S3v4'`.</li><li>`path`: Optional, string. Bucket path lookup supported by the server. Possible options: `'auto'`, `'on'` or `'off'`. Defaults to `'auto'`.</li></ul> | `[]` |
| `minio_client__mc_binary_url` | URL where the `mc` binary is downloaded from. | `https://dl.min.io/client/mc/release/linux-amd64/mc` |

Example:
```yaml
# optional
minio_client__aliases__group_var: []
minio_client__aliases__host_var:
  - name: 'my-source'
    url: 'https://example.com'
    access_key: 'linuxfabrik'
    secret_key: 'linuxfabrik'
minio_client__mc_binary_url: 'https://dl.min.io/client/mc/release/linux-amd64/mc'
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
