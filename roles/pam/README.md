# Ansible Role linuxfabrik.lfops.pam

This role installs and configures PAM (Pluggable Authentication Modules) according to CIS Rocky Linux 9 Benchmark v2.0.0, section 5.3. It installs the required packages, creates a custom authselect profile, and deploys configuration for `faillock`, `pwquality`, and `pwhistory`. This role enforces pwquality checks for root.


## Tags

| Tag | What it does | Reload / Restart |
| --- | ------------ | ---------------- |
| `pam` | Installs pam, authselect, and libpwquality, and runs all configuration tasks | - |


## Mandatory Role Variables

This role does not have any mandatory variables.


## Optional Role Variables

| Variable | Description | Default Value |
| -------- | ----------- | ------------- |
| `pam__authselect_profile` | Name of the custom authselect profile to create and select. If unset, the authselect configuration is skipped entirely. | unset |
| `pam__faillock_deny` | Number of consecutive failed authentication attempts before the account is locked. Must be 5 or less. | `5` |
| `pam__faillock_unlock_time` | Time in seconds before a locked account is automatically unlocked. Use `0` to never auto-unlock (requires manual `faillock --reset`), or a value of `900` or greater. | `0` |
| `pam__faillock_root_unlock_time` | Time in seconds before the root account is unlocked after being locked. Implies `even_deny_root`. Must be `60` or greater. | `60` |
| `pam__pwquality_difok` | Number of characters in the new password that must not be present in the old password. Must be `2` or more. | `2` |
| `pam__pwquality_minlen` | Minimum acceptable length for the new password. Must be `14` or more. | `14` |
| `pam__pwquality_minclass` | Minimum number of character classes required in the new password (digits, uppercase, lowercase, other). | `4` |
| `pam__pwquality_dcredit` | Maximum credit for digits. A negative value sets the minimum number of digits required. | `-1` |
| `pam__pwquality_ucredit` | Maximum credit for uppercase characters. A negative value sets the minimum number required. | `-1` |
| `pam__pwquality_lcredit` | Maximum credit for lowercase characters. A negative value sets the minimum number required. | `-1` |
| `pam__pwquality_ocredit` | Maximum credit for other characters. A negative value sets the minimum number required. | `-1` |
| `pam__pwquality_maxrepeat` | Maximum number of allowed consecutive identical characters. Must be between `1` and `3`. | `3` |
| `pam__pwquality_maxsequence` | Maximum length of allowed monotonic character sequences (e.g. `12345`, `fedcb`). Must be between `1` and `3`. | `3` |
| `pam__pwhistory_remember` | Number of previous passwords to remember per user. Must be `24` or more. | `24` |

Example:
```yaml
# optional
pam__authselect_profile: 'custom-profile'  # omit to skip authselect configuration
pam__faillock_deny: 5
pam__faillock_unlock_time: 0
pam__faillock_root_unlock_time: 60
pam__pwquality_difok: 2
pam__pwquality_minlen: 14
pam__pwquality_minclass: 4
pam__pwquality_dcredit: -1
pam__pwquality_ucredit: -1
pam__pwquality_lcredit: -1
pam__pwquality_ocredit: -1
pam__pwquality_maxrepeat: 3
pam__pwquality_maxsequence: 3
pam__pwhistory_remember: 24
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
