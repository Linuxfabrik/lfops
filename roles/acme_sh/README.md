# Ansible Role linuxfabrik.lfops.acme_sh

This role installs [acme.sh](https://github.com/acmesh-official/acme.sh) and enables issuing certificates with [Let's Encrypt](https://letsencrypt.org). Issued certificates are copied from `/etc/acme.sh` to `/etc/pki/tls/` (Red Hat family) or `/etc/ssl/` (Debian and Ubuntu).

Reference them in an Apache HTTPd vHost as follows (Red Hat family):
```
SSLEngine on
SSLCertificateFile      /etc/pki/tls/certs/www.example.com.crt
SSLCertificateKeyFile   /etc/pki/tls/private/www.example.com.key
SSLCertificateChainFile /etc/pki/tls/certs/www.example.com-chain.crt
```


*Available since LFOps `2.0.0`.*


## How the Role Behaves

Certificates are issued with the key type set by `acme_sh__key_length`, which defaults to ECDSA P-256 (`ec-256`). ECDSA P-256 offers security equivalent to RSA-3072 at a lower handshake cost and is universally supported by current clients. A certificate that was previously issued as RSA is reissued as ECDSA: acme.sh keeps RSA and ECDSA certificates in separate stores, so the ECDSA certificate is issued next to the existing RSA one and then installed to the same paths under `/etc/pki/`. Apache picks up the new certificate on reload without any vHost change. The superseded RSA certificate is dropped from acme.sh's renewal list, and its files are left in place. To keep issuing RSA, set `acme_sh__key_length` to an RSA value such as `4096`.

The role installs a certificate and runs the reload command only when it just (re)issued that certificate, or when the installed file differs from the one acme.sh issued (self-heal). It does not reinstall and reload on every run. Ongoing renewals are installed and reloaded by acme.sh itself, driven by the `acme-sh` systemd timer, using the paths saved at install time.

A vHost that references a certificate before it is issued keeps Apache HTTPd from starting, while acme.sh needs a running web server to answer the HTTP-01 challenge. The `apache_httpd` playbook and the `setup_*` playbooks that contain `apache_httpd` therefore have `apache_httpd` create a self-signed placeholder at every path of `acme_sh__certificates` that does not exist yet, so Apache HTTPd starts, and this role replaces the placeholder at the same path once the certificate is issued. Enable this role in such a playbook with its skip variable (see the [playbooks README](https://github.com/Linuxfabrik/lfops/blob/main/playbooks/README.md)) to get a fresh host up with its certificates in a single run.

Before issuing, the role runs the handlers notified so far in the play, so that a vHost for the ACME challenge that an earlier role just deployed is already served.


## Requirements

* Every name and alternative name in `acme_sh__certificates` resolves to this host, and the host is reachable from the Internet on port 80.
* A web server on this host serves `http://<name>/.well-known/acme-challenge/` from `/var/www/html/letsencrypt/.well-known/acme-challenge/`. With LFOps, a vHost like this one in `apache_httpd__vhosts__host_var` does so:

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
        * Default: `'systemctl reload httpd'` (Red Hat family), `'systemctl reload apache2'` (Debian and Ubuntu)

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
* Default: `reload_cmd` subkey of the `acme_sh__certificates` item, or `'systemctl reload httpd'` (Red Hat family), `'systemctl reload apache2'` (Debian and Ubuntu)

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

**`Request failed: <urlopen error timed out>'`**

* Check if your Reverse Proxy is available over the Internet (Ports on Provider- and Host-Firewall, DNS set correctly, DNAT configured), and check if it is hosting the requested domain on Port 80.

**Replace an issued certificate**

* Run on the control node:

    ```bash
    ansible MYHOST --inventory=$INV --module-name=shell --args "acme.sh --remove --domain www.example.com; rm -rf /etc/acme.sh/certs/www.example.com/"
    ansible-playbook --inventory=$INV linuxfabrik.lfops.acme_sh
    ```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
