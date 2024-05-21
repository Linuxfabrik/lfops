# Ansible Role linuxfabrik.lfops.acme_sh

This role installs [acme.sh](https://github.com/acmesh-official/acme.sh) and enables issuing certificates with [Let's Encrypt](https://letsencrypt.org). Issued certificates are copied from `/etc/acme.sh` to the appropriate subfolders of `/etc/pki/`.

After running this role, configure Apache HTTPd as follows:
```
SSLEngine on
SSLCertificateFile      /etc/pki/tls/certs/www.example.com.crt
SSLCertificateKeyFile   /etc/pki/tls/private/www.example.com.key
SSLCertificateChainFile /etc/pki/tls/certs/www.example.com-chain.crt
```

## Mandatory Requirements

* Install `openssl`. This can be done using the [linuxfabrik.lfops.apps](https://github.com/Linuxfabrik/lfops/tree/main/roles/apps) role.
* Install `tar`. This can be done using the [linuxfabrik.lfops.apps](https://github.com/Linuxfabrik/lfops/tree/main/roles/apps) role.
* Have a configured webserver.

If you use the [acme.sh Playbook](https://github.com/Linuxfabrik/lfops/blob/main/playbooks/acme_sh.yml), this is automatically done for you.


## Tags

| Tag                    | What it does                                  |
| ---                    | ------------                                  |
| `acme_sh`              | Installs acme.sh and issues certificates      |
| `acme_sh:certificates` | Issues certificates                           |
| `acme_sh:state`        | Manages the state of the weekly acme.sh timer |


## Mandatory Role Variables

| Variable                 | Description                                                                           |
| --------                 | -----------                                                                           |
| `acme_sh__account_email` | Email address for the Let's encrypt account. This address will receive expiry emails. |
| `acme_sh__certificates`  | List of certificates that should be issued. Subkeys: <ul><li>`name`: Mandatory, string. Domain of the certificate.</li><li>`alternative_names`: Optional, list. Subject Alternative Names (SAN) for the certificate. Defaults to unset.</li><li>`reload_cmd`: Optional, string. Command to execute after issue/renew to reload the server. Defaults to `systemctl reload httpd`.</li></ul> |

Example:
```yaml
# mandatory
acme_sh__account_email: 'info@example.com'
acme_sh__certificates:
  - name: 'other.example.com'
  - name: 'test.example.com'
    reload_cmd: '/usr/local/sbin/custom_reload_script'
```


## Optional Role Variables

| Variable | Description | Default Value |
| -------- | ----------- | ------------- |
| `acme_sh__deploy_to_host`  | The host which the issued certificates should be deployed to. | unset |
| `acme_sh__deploy_to_host_hook`  | The deployment hook which should be used to deploy the certificates to the deploy host. | `ssh` |
| `acme_sh__deploy_to_host_reload_cmd`  | The reload command which should be executed after the certificates were deployed to the deploy host. | `reload_cmd` subkey of the `acme_sh__certificates` item, or `systemctl reload httpd` |
| `acme_sh__deploy_to_host_user`  | The remote user account which should be used to deploy the certificates to the deploy host. | `root` |
| `acme_sh__key_length`  | Key length in bits of the certificates to issue. | `4096` |
| `acme_sh__timer_enabled` | Enables or disables the weekly acme.sh timer, analogous to `systemctl enable/disable --now`. | `true` |

Example:
```yaml
# optional
acme_sh__deploy_to_host: 'proxy02.example.com'
acme_sh__deploy_to_host_hook: 'ssh'
acme_sh__deploy_to_host_reload_cmd: 'systemctl reload nginx'
acme_sh__deploy_to_host_user: 'root'
acme_sh__key_length: 4096
acme_sh__timer_enabled: true
```


## Troubleshooting

Replace an issued certificate:

```bash
# on the remote host:
acme.sh --remove --domain www.example.com
rm -rf /etc/acme.sh/certs/www.example.com/
```

```bash
# on the control node:
ansible-playbook --inventory $INV linuxfabrik.lfops.acme_sh
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
