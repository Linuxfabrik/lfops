# Ansible Role linuxfabrik.lfops.objectstore_backup

This role configures a backup service/timer for an objectstore to objectstore backup using the 'MinIO' client `mc`.

Runs on

* Rocky 8


## Mandatory Requirements

* Install the `MinIO` binary. This can be done using the [linuxfabrik.lfops.minio_client](https://github.com/Linuxfabrik/lfops/tree/main/roles/minio_client) role.

If you use the [Objectstore Backup Playbook](https://github.com/Linuxfabrik/lfops/blob/main/playbooks/objectstore_backup.yml), this is automatically done for you.


## Tags

| Tag                  | What it does                                   |
| ---                  | ------------                                   |
| `objectstore_backup` | Installs and configures the objectstore backup |


## Mandatory Role Variables

| Variable | Description |
| -------- | ----------- |
| `objectstore_backup__destination_access_key` | S3 and Elastic Compute Cloud (EC2) Access Key for the destination objectstore. |
| `objectstore_backup__destination_secret_key` | S3 and Elastic Compute Cloud (EC2) Access Secret for the destination objectstore. |
| `objectstore_backup__source_access_key` | S3 and Elastic Compute Cloud (EC2) Access Key for the source objectstore. |
| `objectstore_backup__source_secret_key` | S3 and Elastic Compute Cloud (EC2) Access Secret for the source objectstore. |

Example:
```yaml
# mandatory
objectstore_backup__destination_access_key: 'linuxfabrik'
objectstore_backup__destination_secret_key: 'linuxfabrik'
objectstore_backup__source_access_key: 'linuxfabrik'
objectstore_backup__source_secret_key: 'linuxfabrik'
```


## Optional Role Variables

| Variable | Description | Default Value |
| -------- | ----------- | ------------- |
| `objectstore_backup__destination_bucket` | The name of the bucket to be backed-up to at the destination objectstore. Will be created if it does not exist. | `{{ ansible_nodename }}` |
| `objectstore_backup__destination_name` | A unique name (alias) for the destination objectstore. | `swissbackup` |
| `objectstore_backup__destination_url` | The URL that identifies a host and port as the entry point for the destination S3 objectstore web service. | `https://s3.swiss-backup03.infomaniak.com` |
| `objectstore_backup__on_calendar` | The `OnCalendar` definition for when the backup should occur. Have a look at `man systemd.time(7)` for the format. | `Sun *-*-* 19:00:00` |
| `objectstore_backup__source_bucket` | The name of the bucket to be backed-up from the source objectstore | `{{ ansible_nodename }}` |
| `objectstore_backup__source_name` | A unique name (alias) for the source objectstore. | `swisscloud` |
| `objectstore_backup__source_url` | The URL that identifies a host and port as the entry point for the source S3 objectstore web service. | `https://s3.pub1.infomaniak.cloud` |

Example:
```yaml
# optional
objectstore_backup__destination_bucket: '{{ ansible_nodename }}'
objectstore_backup__destination_name: 'swissbackup'
objectstore_backup__destination_url: 'https://s3.swiss-backup03.infomaniak.com'
objectstore_backup__on_calendar: 'Sun *-*-* 19:00:00'
objectstore_backup__source_bucket: '{{ ansible_nodename }}'
objectstore_backup__source_name: 'swisscloud'
objectstore_backup__source_url: 'https://s3.pub1.infomaniak.cloud'
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
