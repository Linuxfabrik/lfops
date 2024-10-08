# Ansible Role linuxfabrik.lfops.postfix

This role installs and configures [postfix](https://www.postfix.org/).


## Tags

| Tag             | What it does                                     |
| ---             | ------------                                     |
| `postfix`       | Installs and configures postfix                  |
| `postfix:state` | Manages the state of the postfix systemd service |


## Mandatory Role Variables

| Variable                      | Description                              |
| --------                      | -----------                              |
| `postfix__relayhost`          | Host name of the mail server.            |

Example:
```yaml
# mandatory
postfix__relayhost: 'mail.example.com:587'
```


## Optional Role Variables

| Variable | Description | Default Value |
| -------- | ----------- | ------------- |
| `postfix__aliases__host_var` / <br> `postfix__aliases__role_var` | List of dictionaries for `/etc/aliases`, a system-wide mechanism to redirect mail for local recipients. Subkeys: <ul><li>`name`: Mandatory, string. The local address (no domain part).</li><li>`value`: Mandatory, string. Generally the redirect address. Have a look at `man aliases` for advanced options.</li><li>`state`: Optional, string. State of the entry. Either `'present'` or `'absent'`. Defaults to `'present'`.</li></ul> | `[]` |
| `postfix__biff` | Boolean. See https://www.postfix.org/postconf.5.html#biff | `false` |
| `postfix__bounce_queue_lifetime` | See https://www.postfix.org/postconf.5.html#bounce_queue_lifetime | `'5d'` |
| `postfix__inet_interfaces` | The local network interface addresses that this mail system receives mail on. | `'127.0.0.1'` |
| `postfix__inet_protocols` | The Internet protocols Postfix will attempt to use when making or accepting connections. Specify one or more of `ipv4` or `ipv6`, separated by whitespace or commas. The form `all` is equivalent to `ipv4, ipv6` or `ipv4`, depending on whether the operating system implements IPv6. | `'all'` |
| `postfix__mailbox_size_limit` | See https://www.postfix.org/postconf.5.html#mailbox_size_limit | `51200000` |
| `postfix__maximal_queue_lifetime` | See https://www.postfix.org/postconf.5.html#maximal_queue_lifetime | `'5d'` |
| `postfix__message_size_limit` | See https://www.postfix.org/postconf.5.html#message_size_limit | `10240000` |
| `postfix__raw` | Multiline string. Raw content which will be appended to the `/etc/postfix/main.cf`. | unset |
| `postfix__recipient_delimiter` | See https://www.postfix.org/postconf.5.html#recipient_delimiter | `''` |
| `postfix__relayhost_password` | Password for the specified user | `''` |
| `postfix__relayhost_username` | Username with access to the mail server. | `'{{ mailto_root__from }}'` |
| `postfix__sender_canonicals__group_var` / <br> `postfix__sender_canonicals__host_var` | List of dictionaries for `/etc/postfix/canonical`, used to rewrite the sender addresses. Subkeys: <ul><li>`pattern`: Mandatory, string. Regular expression to match the entire sender address.</li><li>`address`: Mandatory, string. The rewrite address.</li><li>`state`: Optional, string. State of the entry. Either `'present'` or `'absent'`. Defaults to `'present'`.</li></ul> | `[]` |
| `postfix__service_enabled` | Enables or disables the postfix service, analogous to `systemctl enable/disable`. | `true` |
| `postfix__service_state` | Changes the state of the postfix service, analogous to `systemctl start/stop/restart/reload`. Possible options:<br> * `started`<br> * `stopped`<br> * `restarted`<br> * `reloaded` | `'started'` |
| `postfix__smtp_destination_concurrency_limit` | See https://www.postfix.org/postconf.5.html#smtp_destination_concurrency_limit | `20` |
| `postfix__smtp_destination_recipient_limit` | See https://www.postfix.org/postconf.5.html#smtp_destination_recipient_limit | `50` |
| `postfix__smtp_sasl_auth_enable` | Enable SASL authentication in the Postfix SMTP client. By default, the Postfix SMTP client uses no authentication. | `true` |
| `postfix__smtp_sasl_security_options` | List of Postfix SMTP client SASL security options, separated by commas. Possible options:<br>* `noplaintext`<br>* `noactive`<br>* `nodictionary`<br>* `noanonymous`<br>* `mutual_auth` | `['noplaintext', 'noanonymous']` |
| `postfix__smtp_tls_security_level`| The default SMTP TLS security level for the Postfix SMTP client. When a non-empty value is specified, this overrides the obsolete parameters `smtp_use_tls`, `smtp_enforce_tls`, and `smtp_tls_enforce_peername`; when no value is specified for `smtp_tls_enforce_peername` or the obsolete parameters, the default SMTP TLS security level is `none`. Set this to `'encrypt'` (or stronger) for SMTPS wrappermode (TCP port 465). | `'may'` |
| `postfix__smtp_tls_wrappermode` | Request that the Postfix SMTP client connects using the SUBMISSIONS/SMTPS protocol instead of using the STARTTLS command. This mode requires `postfix__smtp_tls_security_level: 'encrypt'` or stronger. | `false` |

Example:
```yaml
# optional
postfix__aliases__host_var:
  - name: 'root'
    value: 'admin1@example.com,admin@example.com'
    state: 'present'
postfix__biff: false
postfix__bounce_queue_lifetime: '5d'
postfix__inet_interfaces: 'all'
postfix__inet_protocols: 'all'
postfix__mailbox_size_limit: 51200000
postfix__maximal_queue_lifetime: '5d'
postfix__message_size_limit: 10240000
postfix__raw: |-
  todo
postfix__recipient_delimiter: ''
postfix__relayhost_password: ''
postfix__relayhost_username: ''
postfix__sender_canonicals__host_var:
  - pattern: '/^.+@example.com$/'
    address: 'noreply@example.com'
    state: 'present'
postfix__service_enabled: true
postfix__service_state: 'started'
postfix__smtp_destination_concurrency_limit: 20
postfix__smtp_destination_recipient_limit: 50
postfix__smtp_sasl_auth_enable: true
postfix__smtp_sasl_security_options:
  - 'noplaintext'
  - 'noanonymous'
postfix__smtp_tls_security_level: 'encrypt'
postfix__smtp_tls_wrappermode: true
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
