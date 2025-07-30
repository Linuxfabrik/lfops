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
| `postfix__mastercf_entries__host_var` / <br> `postfix__mastercf_entries__group_var` | See https://www.postfix.org/master.5.html <br> Subkeys: <ul><li>`service`: Mandatory, string. The service name syntax depends on the service type as described next.</li><li>`type`: Mandatory, string. Specify one of the service types found in the above link.</li><li>`private`: Mandatory, string. Whether a service is internal to Postfix (pathname starts with private/), or exposed through Postfix command-line tools (path-name starts with public/). Internet (type inet) services can't be private.</li><li>`unpriv`: Mandatory, string. Whether the service runs with root privileges or as the owner of the Postfix system (the owner name is controlled by the mail_owner configuration variable in the main.cf file).</li><li>`chroot`: Mandatory, string. Whether or not the service runs chrooted to the mail queue directory (pathname is controlled by the queue_directory configuration variable in the main.cf file).</li><li>`wakeup`: Mandatory, string. Automatically wake up the named service after the specified number of seconds. The wake up is implemented by connecting to the service and sending a wake up request. A ? at the end of the wake-up time field requests that no wake up events be sent before the first time a service is used. Specify 0 for no automatic wake up.</li><li>`maxproc`: Mandatory, string. The maximum number of processes that may execute this service simultaneously. Specify 0 for no process count limit.</li><li>`command`: Mandatory, string. The command to be executed.</li><li>`arguments`: Mandatory, list. The arguments to execute the commend with.</li>li>`state`: Optional, string. State of the entry. Either `'present'` or `'absent'`. Defaults to `'present'`.</li></ul> | see `vars/` |
| `postfix__maximal_queue_lifetime` | See https://www.postfix.org/postconf.5.html#maximal_queue_lifetime | `'5d'` |
| `postfix__message_size_limit` | See https://www.postfix.org/postconf.5.html#message_size_limit | `10240000` |
| `postfix__mydestination` | See [postfix.org](https://www.postfix.org/postconf.5.html#mydestination) | '$myhostname, localhost.$mydomain, localhost' |
| `postfix__myhostname` | See [postfix.org](https://www.postfix.org/postconf.5.html#myhostname) | unset |
| `postfix__mynetworks` | See https://www.postfix.org/postconf.5.html#mynetworks | `[]` |
| `postfix__myorigin` | See [postfix.org](https://www.postfix.org/postconf.5.html#myorigin) | '$myhostname' |
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
| `postfix__smtp_sasl_mechanism_filter` | List. If non-empty, a Postfix SMTP client filter for the remote SMTP server's list of offered SASL mechanisms. | `[]` |
| `postfix__smtp_sasl_password_maps` | See [postfix.org](https://www.postfix.org/postconf.5.html#smtp_sasl_password_maps) | 'hash:/etc/postfix/sasl_passwd' |
| `postfix__smtp_sasl_security_options` | List of Postfix SMTP client SASL security options, separated by commas. Possible options:<br>* `noplaintext`<br>* `noactive`<br>* `nodictionary`<br>* `noanonymous`<br>* `mutual_auth` | `['noplaintext', 'noanonymous']` |
| `postfix__smtp_tls_security_level`| The default SMTP TLS security level for the Postfix SMTP client. When a non-empty value is specified, this overrides the obsolete parameters `smtp_use_tls`, `smtp_enforce_tls`, and `smtp_tls_enforce_peername`; when no value is specified for `smtp_tls_enforce_peername` or the obsolete parameters, the default SMTP TLS security level is `none`. Set this to `'encrypt'` (or stronger) for SMTPS wrappermode (TCP port 465). | `'may'` |
| `postfix__smtp_tls_wrappermode` | Request that the Postfix SMTP client connects using the SUBMISSIONS/SMTPS protocol instead of using the STARTTLS command. This mode requires `postfix__smtp_tls_security_level: 'encrypt'` or stronger. | `false` |
| `postfix__smtpd_tls_cert_file` | See [postfix.org](https://www.postfix.org/postconf.5.html#smtpd_tls_cert_file) | '/etc/pki/tls/certs/postfix.pem' |
| `postfix__smtpd_tls_key_file` | See [postfix.org](https://www.postfix.org/postconf.5.html#smtpd_tls_key_file) | '/etc/pki/tls/private/postfix.key' |
| `postfix__smtpd_tls_security_level` | See [postfix.org](https://www.postfix.org/postconf.5.html#smtpd_tls_security_level) | 'may' |

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
postfix__mastercf_entries__host_var:
  - service: 'smtps'
    type: 'inet'
    private: 'n'
    unpriv: '-'
    chroot: 'n'
    wakeup: '-'
    maxproc: '-'
    command: 'smtpd'
    arguments:
      - '-o syslog_name=postfix/smtps'
      - '-o smtpd_tls_wrappermode=yes'
      - '-o smtpd_reject_unlisted_recipient=no'
    state: 'present'
  - service: 'maildrop'
    type: 'unix'
    private: '-'
    unpriv: 'n'
    chroot: 'n'
    wakeup: '-'
    maxproc: '-'
    command: 'pipe'
    arguments:
      - 'flags=DRXhu user=vmail argv=/usr/bin/maildrop -d ${recipient}'
    state: 'present'
postfix__maximal_queue_lifetime: '5d'
postfix__message_size_limit: 10240000
postfix__mydestination: '$myhostname, localhost.$mydomain, localhost'
postfix__myhostname: 'mail.example.com'
postfix__mynetworks:
  - '192.0.2.0/24'
postfix__myorigin: '$myhostname'
postfix__raw: |-
  # dovecot
  home_mailbox = mail/
  mailbox_transport = lmtp:unix:/var/run/dovecot/lmtp

  # enable SMTP authentication (via dovecot)
  smtpd_recipient_restrictions = permit_sasl_authenticated, permit_mynetworks, reject_unauth_destination
  smtpd_sasl_auth_enable = yes
  smtpd_sasl_local_domain = $myhostname
  smtpd_sasl_path = private/auth
  smtpd_sasl_security_options = noanonymous
  smtpd_sasl_type = dovecot
  smtpd_tls_auth_only = yes
  # smtpd_tls_loglevel = 1

  # prevent an authenticated client from using a MAIL FROM address that they do not explicitly own and use a blacklist
  smtpd_sender_restrictions = reject_sender_login_mismatch, check_sender_access hash:/etc/postfix/sender_access_blacklist
  # for reject_sender_login_mismatch to work we need to correctly map username@example.com to username
  smtpd_sender_login_maps = regexp:/etc/postfix/sender_login_map

  # DKIM
  smtpd_milters = inet:localhost:8891
  non_smtpd_milters = $smtpd_milters
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
postfix__smtp_sasl_mechanism_filter:
  - 'xoauth2'
postfix__smtp_sasl_password_maps: 'hash:/etc/postfix/sasl_passwd'
postfix__smtp_sasl_security_options:
  - 'noplaintext'
  - 'noanonymous'
postfix__smtp_tls_security_level: 'encrypt'
postfix__smtp_tls_wrappermode: true
postfix__smtpd_tls_cert_file: '/etc/pki/tls/certs/postfix.pem'
postfix__smtpd_tls_key_file: '/etc/pki/tls/private/postfix.key'
postfix__smtpd_tls_security_level: 'may'

```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
