# Ansible Role linuxfabrik.lfops.vsftpd

This role installs and configures [vsftpd](https://security.appspot.com/vsftpd.html), optionally with SSL (FTPS) and user-specific configs.


## Tags

| Tag                | What it does                                                  |
| ---                | ------------                                                  |
| `vsftpd`           | Installs and configures vsftpd                                |
| `vsftpd:configure` | Configues `/etc/vsftpd/vsftpd.conf` and user-specific configs |
| `vsftpd:state`     | Manages the state of the `vsftpd.service`                     |


## Optional Role Variables

| Variable | Description | Default Value |
| -------- | ----------- | ------------- |
| `vsftpd__conf_allow_writeable_chroot` | Boolean. Allow chroot()'ing a user to a directory writable by that user. Note that setting this to YES is potentially dangerous. This setting is only necessary if the root directory of the user's chroot jail itself is writable. Uploading in subfolders works even if this setting is false. | `false`|
| `vsftpd__conf_chroot_local_user` | Boolean. If the user should be placed in a `chroot()` or not. See `man vsftpd.conf`. | `false` |
| `vsftpd__conf_debug_ssl` | Boolean. If true, OpenSSL connection diagnostics are dumped to the vsftpd log file. See `man vsftpd.conf`. | `false` |
| `vsftpd__conf_dual_log_enable` | Boolean. If enabled, two log files are generated in parallel, going by default to `/var/log/xferlog` and `/var/log/vsftpd.log`. See `man vsftpd.conf`. | `false` |
| `vsftpd__conf_guest_enable` | Boolean. If enabled, all non-anonymous logins are classed as "guest" logins. A guest login is remapped to the user specified in the `guest_username` setting. | `false`|
| `vsftpd__conf_guest_username` | String. See the boolean setting `guest_enable` for a description of what constitutes a guest login. This setting is the real username which guest users are mapped to. | `ftp` |
| `vsftpd__conf_local_root` | String. Path to which vsftpd will try to change into after a local (i.e. non-anonymous) login. | unset |
| `vsftpd__conf_log_ftp_protocol` | Boolean. When enabled, all FTP requests and responses are logged, providing the option `vsftpd__conf_xferlog_std_format` is not enabled. Useful for debugging. See `man vsftpd.conf`. | `false` |
| `vsftpd__conf_pasv_addr_resolve` | Boolean. Set to `true` if you want to use a hostname (as opposed to IP address) in `vsftpd__conf_pasv_address`. | `false` |
| `vsftpd__conf_pasv_address` | String. Use this option to override the IP address that vsftpd will advertise in response to the PASV command. Use this when running behind a firewall or loadbalancer. Also see `vsftpd__conf_pasv_addr_resolve`. | unset |
| `vsftpd__conf_pasv_max_port` | Number. The maximum port to allocate for PASV style data connections. `0` means any port. | `0` |
| `vsftpd__conf_pasv_min_port` | Number. The minimum port to allocate for PASV style data connections. `0` means any port. | `0` |
| `vsftpd__conf_rsa_cert_file` | String. Path of the RSA certificate to use for SSL encrypted connections. | `'/usr/share/ssl/certs/vsftpd.pem'` |
| `vsftpd__conf_rsa_private_key_file` | String. Path of the RSA private key to use for SSL encrypted connections. If unset, the private key is expected to be in the same file as the certificate. | unset |
| `vsftpd__conf_session_support` | Boolean. Controls whether vsftpd attempts to maintain sessions for logins using PAM authentication. Use in combination with `vsftpd__pam_use_sss: true` to get users from Active Directory. See `man vsftpd.conf`. | `false` |
| `vsftpd__conf_ssl_enable` | Boolean. If enabled vsftpd will support secure connections via SSL. See `man vsftpd.conf`. | `false` |
| `vsftpd__conf_user_config_dir` | String. Path where the user-specific config should be placed. | `'/etc/vsftpd/user_config'` |
| `vsftpd__conf_user_sub_token` | String. This option is useful is conjunction with virtual users. It is used to automatically generate a home directory for each virtual user, based on a template. For example, if the home directory of the real user specified via guest_username is `/home/virtual/$USER`, and `user_sub_token` is set to `$USER`, then when virtual user fred logs in, he will end up (usually chroot()'ed) in the directory `/home/virtual/fred`. This option also takes affect if `local_root` contains `user_sub_token`. | unset |
| `vsftpd__conf_userlist_deny` | Boolean. This option is examined if `userlist_enable` is activated. If you set this setting to `false`, then users will be denied login unless they are explicitly listed in the file specified by `userlist_file`. When login is denied, the denial is issued before the user is asked for a password. | `true` |
| `vsftpd__conf_userlist_enable` | Boolean. If enabled, vsftpd will load a list of usernames, allowing or denying them based on `userlist_deny`. See `man vsftpd.conf`. | `false` |
| `vsftpd__conf_userlist_log` | Boolean. If enabled, every login denial based on the userlist will be logged. See `man vsftpd.conf`. | `false` |
| `vsftpd__conf_virtual_use_local_privs` | Boolean. If enabled, virtual users will use the same privileges as local users. By default, virtual users will use the same privileges as anonymous users, which tends to be more restrictive (especially in terms of write access). | `false` |
| `vsftpd__conf_xferlog_std_format` | Boolean. If enabled, the transfer log file will be written in standard xferlog format, as used by wu-ftpd, which is less readable but can be parsed by existing tools. See `man vsftpd.conf`. | `false` |
| `vsftpd__pam_use_sss`| Boolean. If true, SSSD will be used during PAM authentication. Use in combination with `vsftpd__conf_session_support: true` to get users from Active Directory. | `false` |
| `vsftpd__service_enabled` | Boolean. Enables or disables the service, analogous to `systemctl enable/disable --now`. | `true` |
| `vsftpd__user_config__host_var` / <br> `vsftpd__user_config__group_var` | List of dictionaries. Set user-specific configs, especially useful for the chroot directory (`local_root`). Note: When using a default Active Directory domain in sssd, user configs are required to cover the username with and without the domain. Subkeys: <ul><li>`name`: Mandatory, string. The username to which the config applies.</li><li>`raw`: Optional, multiline string. Raw content.</li><li>`state`: Optional, string. State of the config, one of `present`, `absent`. Defaults to `present`.</li><li>`template`: Mandatory, string. Template to use. One of `raw`.</li></ul> | `[]` |

Example:
```yaml
# optional
vsftpd__conf_allow_writeable_chroot: false
vsftpd__conf_chroot_local_user: true
vsftpd__conf_debug_ssl: true
vsftpd__conf_dual_log_enable: true
vsftpd__conf_guest_enable: false
vsftpd__conf_guest_username: 'ftp'
vsftpd__conf_local_root: '/data'
vsftpd__conf_log_ftp_protocol: true
vsftpd__conf_pasv_addr_resolve: true
vsftpd__conf_pasv_address: 'ftp.example.com'
vsftpd__conf_pasv_max_port: 51000
vsftpd__conf_pasv_min_port: 50000
vsftpd__conf_rsa_cert_file: '/etc/pki/tls/certs/vsftpd.pem'
vsftpd__conf_rsa_private_key_file: '/etc/pki/tls/private/vsftpd.key'
vsftpd__conf_session_support: true
vsftpd__conf_ssl_enable: true
vsftpd__conf_user_config_dir: '/etc/vsftpd/user_config'
vsftpd__conf_user_sub_token: '$USER'
vsftpd__conf_userlist_deny: true
vsftpd__conf_userlist_enable: false
vsftpd__conf_userlist_log: true
vsftpd__conf_virtual_use_local_privs: false
vsftpd__conf_xferlog_std_format: false

vsftpd__service_enabled: true

vsftpd__user_config__host_var:
  - name: 'user1@example.com'
    template: 'raw'
    state: 'present'
    raw: |-
      local_root=/data/share1
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
