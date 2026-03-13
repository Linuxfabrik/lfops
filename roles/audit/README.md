# Ansible Role linuxfabrik.lfops.audit

This role installs and configures [audit](http://people.redhat.com/sgrubb/audit/), including the daemon's logrotating behaviour.


## Tags

| Tag           | What it does                               | Reload / Restart |
| ---           | ------------                               | ---------------- |
| `audit`       | Installs and configures audit              | - |
| `audit:state` | Starts, stops or restarts the audit daemon | - |


## Optional Role Variables

| Variable | Description | Default Value |
| -------- | ----------- | ------------- |
| `audit__action_mail_account` | This option should contain a valid email address or alias.  The  default   address  is root.  If  the email address is not local to the machine, you must make sure you have email properly configured on your machine and network.  Also,  this  option  requires that /usr/lib/sendmail exists on the machine. | `'root'` |
| `audit__admin_space_left` | This  is  a  numeric value in megabytes that tells the audit daemon when to perform a configurable action because the system is running low on disk space. This  should  be considered  the last chance to do something before running out of disk space. The nu‐ meric value for this parameter should be lower than the number  for  space_left.  You may  also append a percent sign (e.g. 1%) to the number to have the audit daemon cal‐ culate the number based on the disk partition size. | `'10%'` |
| `audit__admin_space_left_action` | This parameter tells the system what action to take when the system has detected that it  is low on disk space.  Valid values are ignore, syslog, rotate, email, exec, sus‐ pend, single, and halt.  If set to ignore, the audit  daemon  does  nothing.   Syslog means  that  it  will issue a warning to syslog.  rotate will rotate logs, losing the oldest to free up space.  Email means that it will send a warning to  the  email  ac‐ count  specified  in action_mail_acct as well as sending the message to syslog.  exec /path-to-script will execute the script. You cannot pass parameters  to  the  script. The  script  is also responsible for telling the auditd daemon to resume logging once its completed its action. This can be done by adding service  auditd  resume  to  the script.  Suspend will cause the audit daemon to stop writing records to the disk. The daemon will still be alive. The single option will cause the audit daemon to put  the computer  system  in single user mode. The halt option will cause the audit daemon to shutdown the computer system. Except for rotate, it will perform this action just one time. | `'EMAIL'` |
| `audit__num_logs` | This  keyword  specifies  the  number  of log files to keep if rotate is given as the max_log_file_action.  If the number is < 2, logs are not rotated. This number must be 999  or less.  The default is 0 - which means no rotation. As you increase the number of log files being rotated, you may need to adjust the kernel backlog setting upwards since  it  takes  more  time  to rotate the files. This is typically done in /etc/au‐ dit/audit.rules. If log rotation is configured to occur, the daemon  will  check  for excess  logs  and  remove them in effort to keep disk space available. The excess log check is only done on startup and when a reconfigure results in a space check. | `10` |
| `audit__space_left` | If  the  free space in the filesystem containing log_file drops below this value, the audit daemon takes the action  specified  by  space_left_action.   If  the  value  of space_left  is  specified as a whole number, it is interpreted as an absolute size in megabytes (MiB).  If the value is specified as a number between 1 and 99 followed  by a  percentage  sign  (e.g.,  5%),  the  audit  daemon calculates the absolute size in megabytes based on the size of the filesystem containing  log_file.   (E.g.,  if  the filesystem  containing log_file is 2 gigabytes in size, and space_left is set to 25%, then the audit daemon sets space_left to approximately 500 megabytes.  Note that this calculation  is performed when the audit daemon starts, so if you resize the filesys‐ tem containing log_file while the audit daemon is running, you should send the  audit daemon  SIGHUP to re-read the configuration file and recalculate the correct percent‐ age. | `'20%'` |
| `audit__space_left_action` | This parameter tells the system what action to take when the system has detected that it  is  starting  to get low on disk space.  Valid values are ignore, syslog, rotate, email, exec, suspend, single, and halt.  If set to  ignore,  the  audit  daemon  does nothing.   syslog  means  that it will issue a warning to syslog.  rotate will rotate logs, losing the oldest to free up space.  Email means that it will send a warning to the  email  account  specified  in action_mail_acct as well as sending the message to syslog.  exec /path-to-script will execute the script. You cannot pass parameters  to the  script.  The  script is also responsible for telling the auditd daemon to resume logging once its completed its action. This can be done by adding service auditd  re‐ sume  to  the script.  suspend will cause the audit daemon to stop writing records to the disk. The daemon will still be alive. The single option will cause the audit dae‐ mon  to  put  the computer system in single user mode. The halt option will cause the audit daemon to shutdown the computer system. Except for rotate, it will perform this action just one time. | `'ROTATE'` |
| `audit__service_enabled` | Enables or disables the auditd service, analogous to `systemctl enable/disable --now`. | `true` |

Example:
```yaml
# optional
audit__action_mail_account: 'root'
audit__admin_space_left: '10%'
audit__admin_space_left_action: 'EMAIL'
audit__num_logs: 10
audit__space_left: '20%'
audit__space_left_action: 'ROTATE'
audit__service_enabled: true
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
