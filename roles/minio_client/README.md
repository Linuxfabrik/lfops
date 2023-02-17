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
| `minio_client__mc_binary_url` | URL where the `mc` binary is downloaded from. | `https://dl.min.io/client/mc/release/linux-amd64/mc` |

Example:
```yaml
# optional
minio_client__mc_binary_url: 'https://dl.min.io/client/mc/release/linux-amd64/mc'
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
