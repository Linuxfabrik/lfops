# Ansible Role linuxfabrik.lfops.acme_sh

This role installs [acme.sh](https://github.com/acmesh-official/acme.sh) and enables issuing certificates with [Let's Encrypt](https://letsencrypt.org). Issued certificates are copied from `/etc/acme.sh` to the appropriate subfolders of `/etc/pki/`.

After running this role, configure Apache HTTPd as follows:
```
SSLEngine on
SSLCertificateFile      /etc/pki/tls/certs/www.example.com.crt
SSLCertificateKeyFile   /etc/pki/tls/private/www.example.com.key
SSLCertificateChainFile /etc/pki/tls/certs/www.example.com-chain.crt
```


*Available since LFOps `2.0.0`.*


## How the Role Behaves

Certificates are issued with the key type set by `acme_sh__key_length`, which defaults to ECDSA P-256 (`ec-256`). ECDSA P-256 offers security equivalent to RSA-3072 at a lower handshake cost and is universally supported by current clients. A certificate that was previously issued as RSA is reissued as ECDSA: acme.sh keeps RSA and ECDSA certificates in separate stores, so the ECDSA certificate is issued next to the existing RSA one and then installed to the same paths under `/etc/pki/`. Apache picks up the new certificate on reload without any vHost change. The superseded RSA certificate is dropped from acme.sh's renewal list, and its files are left in place. To keep issuing RSA, set `acme_sh__key_length` to an RSA value such as `4096`.

The role installs a certificate to `/etc/pki/` and runs the reload command only when it just (re)issued that certificate, or when the installed file is missing (self-heal). It does not reinstall and reload on every run. Ongoing renewals are installed and reloaded by acme.sh itself, driven by the `acme-sh` systemd timer, using the paths saved at install time.


## Dependent Roles

Any [LFOps playbook](https://github.com/Linuxfabrik/lfops/blob/main/playbooks/README.md) that installs this role runs these for you. Optional ones can be disabled via the playbook's skip variables.

* `openssl` must be installed (role: [linuxfabrik.lfops.apps](https://github.com/Linuxfabrik/lfops/tree/main/roles/apps)).
* `tar` must be installed (role: [linuxfabrik.lfops.apps](https://github.com/Linuxfabrik/lfops/tree/main/roles/apps)).


## Requirements

Manual steps:

* Configure a web server. The playbook does not set this up. If you are using LFOps to manage an Apache reverse proxy, a virtual host working for acme might be defined like this:

```yaml
apache_httpd__vhosts__host_var:
  - conf_server_name: 'www.example.com'
    enabled: true
    state: 'present'
    template: 'redirect'
    virtualhost_port: 80
```


## Tags

`acme_sh`

* Installs acme.sh and issues certificates.
* Triggers: none.

`acme_sh:certificates`

* Issues certificates.
* Triggers: none.

`acme_sh:state`

* Manages the state of the weekly acme.sh timer.
* Triggers: none.


## Mandatory Role Variables

`acme_sh__account_email`

* Email address for the Let's encrypt account. This address will receive expiry emails.
* Type: String.
* Default: none

`acme_sh__certificates`

* List of certificates that should be issued.
* Type: List of dictionaries.
* Default: none
* Subkeys:

    * `name`:

        * Mandatory. Domain of the certificate.
        * Type: String.

    * `alternative_names`:

        * Optional. Subject Alternative Names (SAN) for the certificate.
        * Type: List.
        * Default: unset

    * `reload_cmd`:

        * Optional. Command to execute after issue/renew to reload the server.
        * Type: String.
        * Default: `'systemctl reload httpd'`

Example:
```yaml
# mandatory
acme_sh__account_email: 'info@example.com'
acme_sh__certificates:
  - name: 'other.example.com'
  - name: 'test.example.com'
    alternative_names:
      - 'linuxfabrik.example.com'
    reload_cmd: '/usr/local/sbin/custom_reload_script'
```


## Optional Role Variables

`acme_sh__deploy_to_host`

* The host which the issued certificates should be deployed to.
* Type: String.
* Default: unset

`acme_sh__deploy_to_host_hook`

* The deployment hook which should be used to deploy the certificates to the deploy host.
* Type: String.
* Default: `'ssh'`

`acme_sh__deploy_to_host_reload_cmd`

* The reload command which should be executed on the deploy host after the certificates were deployed to the deploy host.
* Type: String.
* Default: `reload_cmd` subkey of the `acme_sh__certificates` item, or `'systemctl reload httpd'`

`acme_sh__deploy_to_host_user`

* The remote user account which should be used to deploy the certificates to the deploy host.
* Type: String.
* Default: `'root'`

`acme_sh__key_length`

* Key type and length of the certificates to issue. RSA: `2048`, `3072`, `4096`. ECDSA: `ec-256` (P-256), `ec-384` (P-384), `ec-521` (P-521).
* Type: String.
* Default: `'ec-256'`

`acme_sh__reload_cmd`

* The reload command which should be executed on the local host after the certificates were installed.
* Type: String.
* Default: `reload_cmd` subkey of the `acme_sh__certificates` item, or `'systemctl reload httpd'`

`acme_sh__timer_enabled`

* Enables or disables the weekly acme.sh timer, analogous to `systemctl enable/disable --now`.
* Type: Bool.
* Default: `true`

Example:
```yaml
# optional
acme_sh__deploy_to_host: 'proxy02.example.com'
acme_sh__deploy_to_host_hook: 'ssh'
acme_sh__deploy_to_host_reload_cmd: 'systemctl reload nginx'
acme_sh__deploy_to_host_user: 'root'
acme_sh__key_length: 'ec-256'
acme_sh__timer_enabled: true
acme_sh__reload_cmd: 'systemctl reload nginx'
```


## Troubleshooting

`Request failed: <urlopen error timed out>'`: Check if your Reverse Proxy is available over the Internet (Ports on Provider- and Host-Firewall, DNS set correctly, DNAT configured), and check if it is hosting the requested domain on Port 80.

Replace an issued certificate:

```bash
# on the control node:
ansible MYHOST --inventory=$INV --module-name=shell --args "acme.sh --remove --domain www.example.com; rm -rf /etc/acme.sh/certs/www.example.com/"
ansible-playbook --inventory=$INV linuxfabrik.lfops.acme_sh
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
