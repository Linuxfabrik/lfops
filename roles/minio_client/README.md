# Ansible Role linuxfabrik.lfops.minio_client

This role installs the MinIO client binary, including bash completion and sets config location to `/etc/mc/`.


## Tags

`minio_client`

* Installs and configures MinIO client.
* Triggers: none.

`minio_client:configure`

* Configures MinIO client.
* Triggers: none.


## Optional Role Variables

`minio_client__aliases__group_var` / `minio_client__aliases__host_var`

* List of MinIO connection aliases.
* Subkeys:

    * `name`:

        * Mandatory. Name of the alias. Has to be unique.
        * Type: String.

    * `access_key`:

        * Mandatory. The S3 and Elastic Compute Cloud (EC2) Access Key.
        * Type: String.

    * `secret_key`:

        * Mandatory. The S3 and Elastic Compute Cloud (EC2) Secret Key.
        * Type: String.

    * `api`:

        * Optional. The API signature. Possible options: `'S3v4'` or `'S3v2'`.
        * Type: String.
        * Default: `'S3v4'`

    * `path`:

        * Optional. Bucket path lookup supported by the server. Possible options: `'auto'`, `'on'` or `'off'`.
        * Type: String.
        * Default: `'auto'`

    * `state`:

        * Optional. Either `present` or `absent`.
        * Type: String.
        * Default: `'present'`

* Type: List of dictionaries.
* Default: `[]`

`minio_client__mc_binary_url`

* URL where the `mc` binary is downloaded from.
* Type: String.
* Default: `'https://dl.min.io/client/mc/release/linux-amd64/mc'`

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
