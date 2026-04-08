# Ansible Role linuxfabrik.lfops.postfix

This role installs and configures [postfix](https://www.postfix.org/).


## Tags

`postfix`

* Installs and configures postfix.
* Triggers: postfix.service reload.

`postfix:state`

* Manages the state of the postfix systemd service.
* Triggers: none.


## Mandatory Role Variables

`postfix__relayhost`

* Host name of the mail server.
* Type: String.

Example:
```yaml
# mandatory
postfix__relayhost: 'mail.example.com:587'
```


## Optional Role Variables

`postfix__aliases__host_var` / `postfix__aliases__group_var`

* List of dictionaries for `/etc/aliases`, a system-wide mechanism to redirect mail for local recipients.
* For the usage in `host_vars` / `group_vars` (can only be used in one group at a time).
* Type: List of dictionaries.
* Default: `[]`
* Subkeys:

    * `name`:

        * Mandatory. The local address (no domain part).
        * Type: String.

    * `value`:

        * Mandatory. Generally the redirect address. Have a look at `man aliases` for advanced options.
        * Type: String.

    * `state`:

        * Optional. State of the entry. Either `'present'` or `'absent'`.
        * Type: String.
        * Default: `'present'`

`postfix__biff`

* See https://www.postfix.org/postconf.5.html#biff
* Type: Bool.
* Default: `false`

`postfix__bounce_queue_lifetime`

* See https://www.postfix.org/postconf.5.html#bounce_queue_lifetime
* Type: String.
* Default: `'5d'`

`postfix__inet_interfaces`

* The local network interface addresses that this mail system receives mail on.
* Type: String.
* Default: `'127.0.0.1'`

`postfix__inet_protocols`

* The Internet protocols Postfix will attempt to use when making or accepting connections. Specify one or more of `ipv4` or `ipv6`, separated by whitespace or commas. The form `all` is equivalent to `ipv4, ipv6` or `ipv4`, depending on whether the operating system implements IPv6.
* Type: String.
* Default: `'all'`

`postfix__lookup_tables__host_var` / `postfix__lookup_tables__group_var`

* List of dictionaries containing [Postfix Lookup Tables](https://www.postfix.org/DATABASE_README.html). The role automatically runs `postmap` if the table changed.
* For the usage in `host_vars` / `group_vars` (can only be used in one group at a time).
* Type: List of dictionaries.
* Default: `[]`
* Subkeys:

    * `path`:

        * Mandatory. Path to the lookup table. Can be used in `postfix__raw`.
        * Type: String.

    * `content`:

        * Mandatory. Content of the lookup table.
        * Type: String.

    * `state`:

        * Optional. State of the lookup table. Either `'present'` or `'absent'`.
        * Type: String.
        * Default: `'present'`

`postfix__mailbox_size_limit`

* See https://www.postfix.org/postconf.5.html#mailbox_size_limit
* Type: Number.
* Default: `51200000`

`postfix__mastercf_entries__host_var` / `postfix__mastercf_entries__group_var`

* See https://www.postfix.org/master.5.html
* For the usage in `host_vars` / `group_vars` (can only be used in one group at a time).
* Type: List of dictionaries.
* Default: see `vars/`
* Subkeys:

    * `service`:

        * Mandatory. The service name syntax depends on the service type as described next.
        * Type: String.

    * `type`:

        * Mandatory. Specify one of the service types found in the above link.
        * Type: String.

    * `private`:

        * Mandatory. Whether a service is internal to Postfix (pathname starts with private/), or exposed through Postfix command-line tools (path-name starts with public/). Internet (type inet) services can't be private.
        * Type: String.

    * `unpriv`:

        * Mandatory. Whether the service runs with root privileges or as the owner of the Postfix system (the owner name is controlled by the mail_owner configuration variable in the main.cf file).
        * Type: String.

    * `chroot`:

        * Mandatory. Whether or not the service runs chrooted to the mail queue directory (pathname is controlled by the queue_directory configuration variable in the main.cf file).
        * Type: String.

    * `wakeup`:

        * Mandatory. Automatically wake up the named service after the specified number of seconds. The wake up is implemented by connecting to the service and sending a wake up request. A ? at the end of the wake-up time field requests that no wake up events be sent before the first time a service is used. Specify 0 for no automatic wake up.
        * Type: String.

    * `maxproc`:

        * Mandatory. The maximum number of processes that may execute this service simultaneously. Specify 0 for no process count limit.
        * Type: String.

    * `command`:

        * Mandatory. The command to be executed.
        * Type: String.

    * `arguments`:

        * Mandatory. The arguments to execute the command with.
        * Type: List.

    * `state`:

        * Optional. State of the entry. Either `'present'` or `'absent'`.
        * Type: String.
        * Default: `'present'`

`postfix__maximal_queue_lifetime`

* See https://www.postfix.org/postconf.5.html#maximal_queue_lifetime
* Type: String.
* Default: `'5d'`

`postfix__message_size_limit`

* See https://www.postfix.org/postconf.5.html#message_size_limit
* Type: Number.
* Default: `10240000`

`postfix__mydestination`

* See [postfix.org](https://www.postfix.org/postconf.5.html#mydestination)
* Type: String.
* Default: `'$myhostname, localhost.$mydomain, localhost'`

`postfix__myhostname`

* See [postfix.org](https://www.postfix.org/postconf.5.html#myhostname)
* Type: String.
* Default: unset

`postfix__mynetworks`

* See https://www.postfix.org/postconf.5.html#mynetworks
* Type: List.
* Default: `[]`

`postfix__myorigin`

* See [postfix.org](https://www.postfix.org/postconf.5.html#myorigin)
* Type: String.
* Default: `'$myhostname'`

`postfix__raw`

* Raw content which will be appended to the `/etc/postfix/main.cf`.
* Type: Multiline string.
* Default: unset

`postfix__recipient_delimiter`

* See https://www.postfix.org/postconf.5.html#recipient_delimiter
* Type: String.
* Default: `''`

`postfix__relayhost_password`

* Password for the specified user.
* Type: String.
* Default: `''`

`postfix__relayhost_username`

* Username with access to the mail server.
* Type: String.
* Default: `'{{ mailto_root__from }}'`

`postfix__sender_canonicals__group_var` / `postfix__sender_canonicals__host_var`

* List of dictionaries for `/etc/postfix/canonical`, used to rewrite the sender addresses.
* For the usage in `host_vars` / `group_vars` (can only be used in one group at a time).
* Type: List of dictionaries.
* Default: `[]`
* Subkeys:

    * `pattern`:

        * Mandatory. Regular expression to match the entire sender address.
        * Type: String.

    * `address`:

        * Mandatory. The rewrite address.
        * Type: String.

    * `state`:

        * Optional. State of the entry. Either `'present'` or `'absent'`.
        * Type: String.
        * Default: `'present'`

`postfix__service_enabled`

* Enables or disables the postfix service, analogous to `systemctl enable/disable`.
* Type: Bool.
* Default: `true`

`postfix__service_state`

* Changes the state of the postfix service, analogous to `systemctl start/stop/restart/reload`. Possible options: `started`, `stopped`, `restarted`, `reloaded`.
* Type: String.
* Default: `'started'`

`postfix__smtp_destination_concurrency_limit`

* See https://www.postfix.org/postconf.5.html#smtp_destination_concurrency_limit
* Type: Number.
* Default: `20`

`postfix__smtp_destination_recipient_limit`

* See https://www.postfix.org/postconf.5.html#smtp_destination_recipient_limit
* Type: Number.
* Default: `50`

`postfix__smtp_sasl_auth_enable`

* Enable SASL authentication in the Postfix SMTP client. By default, the Postfix SMTP client uses no authentication.
* Type: Bool.
* Default: `true`

`postfix__smtp_sasl_mechanism_filter`

* If non-empty, a Postfix SMTP client filter for the remote SMTP server's list of offered SASL mechanisms.
* Type: List.
* Default: `[]`

`postfix__smtp_sasl_password_maps`

* See [postfix.org](https://www.postfix.org/postconf.5.html#smtp_sasl_password_maps)
* Type: String.
* Default: `'{{ __postfix__map_type }}:/etc/postfix/sasl_passwd'`

`postfix__smtp_sasl_security_options`

* List of Postfix SMTP client SASL security options. Possible options: `noplaintext`, `noactive`, `nodictionary`, `noanonymous`, `mutual_auth`.
* Type: List.
* Default: `['noanonymous']`

`postfix__smtp_tls_security_level`

* The default SMTP TLS security level for the Postfix SMTP client. When a non-empty value is specified, this overrides the obsolete parameters `smtp_use_tls`, `smtp_enforce_tls`, and `smtp_tls_enforce_peername`; when no value is specified for `smtp_tls_enforce_peername` or the obsolete parameters, the default SMTP TLS security level is `none`. Set this to `'encrypt'` (or stronger) for SMTPS wrappermode (TCP port 465).
* Type: String.
* Default: `'may'`

`postfix__smtp_tls_wrappermode`

* Request that the Postfix SMTP client connects using the SUBMISSIONS/SMTPS protocol instead of using the STARTTLS command. This mode requires `postfix__smtp_tls_security_level: 'encrypt'` or stronger.
* Type: Bool.
* Default: `false`

`postfix__smtpd_tls_cert_file`

* See [postfix.org](https://www.postfix.org/postconf.5.html#smtpd_tls_cert_file)
* Type: String.
* Default: `'/etc/pki/tls/certs/postfix.pem'`

`postfix__smtpd_tls_key_file`

* See [postfix.org](https://www.postfix.org/postconf.5.html#smtpd_tls_key_file)
* Type: String.
* Default: `'/etc/pki/tls/private/postfix.key'`

`postfix__smtpd_tls_security_level`

* See [postfix.org](https://www.postfix.org/postconf.5.html#smtpd_tls_security_level)
* Type: String.
* Default: `'may'`

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
postfix__lookup_tables__host_var:
  - path: '/etc/postfix/sender_access_blacklist'
    content: |
        spam.example.com DISCARD
    state: 'present'
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
