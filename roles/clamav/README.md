# Ansible Role linuxfabrik.lfops.clamav

This role installs and configures [ClamAV](https://www.clamav.net/), "an open-source antivirus engine for detecting trojans, viruses, malware & other malicious threats." It also configures freshclam to regularly update the official ClamAV signatures (12 times a day).
This role exposes options for enabling on-access scanning and / or periodic full-scans and configures mail notifications for found viruses.

When using on-access scanning, one might need to increase the `inotify/max_user_watches`. Have a look at the [official documentation](https://docs.clamav.net/manual/OnAccess.html?highlight=inotify#troubleshooting). This can be done using the [linuxfabrik.lfops.kernel_settings](https://github.com/linuxfabrik/lfops/tree/main/roles/kernel_settings) role.
ClamAV can be tested using the EICAR test virus:
```bash
wget http://www.eicar.org/download/eicar.com
wget http://www.eicar.org/download/eicar.com.txt
wget http://www.eicar.org/download/eicar_com.zip
wget http://www.eicar.org/download/eicarcom2.zip
```


## Optional Requirements

* Enable the `antivirus_can_scan_system` and `antivirus_use_jit` SELinux Booleans. This can be done using the [linuxfabrik.lfops.selinux](https://github.com/linuxfabrik/lfops/tree/main/roles/selinux) role.
* Fangfrisch to download unofficial signatures. This can be done using the [linuxfabrik.lfops.fangfrisch](https://github.com/linuxfabrik/lfops/tree/main/roles/fangfrisch) role.

If you use the [ClamAV Playbook](https://github.com/Linuxfabrik/lfops/blob/main/playbooks/clamav.yml), this is automatically done for you.


## Tags

| Tag                | What it does                                             | Reload / Restart |
| ---                | ------------                                             | ---------------- |
| `clamav`           | Installs and configures ClamAV                           | Restarts clamav-clamonacc.service |
| `clamav:state`     | Manages the states of various ClamAV services and timers | - |
| `clamav:configure` | Manages the various ClamAV config files                  | Restarts clamav-clamonacc.service, clamd@scan.service |


## Optional Role Variables

| Variable | Description | Default Value |
| -------- | ----------- | ------------- |
| `clamav__clamd_service_enabled` | Enables or disables the clamd background service, analogous to `systemctl enable/disable`. The clamd service is required for on-access scanning and full-scans. | `true` |
| `clamav__clamdscan_on_calendar` | When the full-scan should be run. Have a look at [systemd.time(7)](https://www.freedesktop.org/software/systemd/man/systemd.time.html) for the format. | `'*-*-* 21:{{ 59 | random(seed=inventory_hostname) }}'` |
| `clamav__clamdscan_paths` | Which paths should be scanned during the full-scan. | `'{{ clamav__scan_on_access_include_paths }}'` |
| `clamav__clamdscan_timer_enabled` | Enables or disables the clamdscan timer for the periodic full-scan, analogous to `systemctl enable/disable`. | `false` |
| `clamav__clamonacc_service_enabled` | Enables or disables the on-access scanning service, analogous to `systemctl enable/disable`. | `false` |
| `clamav__freshclam_private_mirror` | "This option allows you to easily point freshclam to private mirrors" (see `man freshclam.conf`). | `[]` |
| `clamav__freshclam_service_enabled` | Enables or disables the freshclam service, analogous to `systemctl enable/disable`. Freshclam is responsible for updating the official ClamAV signatures. | `true` |
| `clamav__mail_from` | Username with access to the mail server. Required to send mail notifications for found viruses. | `'{{ mailto_root__from }}'` |
| `clamav__mail_recipients` | List recipient addresses to which the mail notifications should be sent. | `'{{ mailto_root__to }}'` |
| `clamav__mail_subject_prefix` | This will set a prefix that will be showed in front of the hostname. Can be used to separate servers by environment or customer. | `''` |
| `clamav__scan_alert_broken_executables` | "With this option clamav will try to detect broken executables (both PE and ELF) and alert on them with the Broken.Executable heuristic signature." | `true` |
| `clamav__scan_detect_pua` | On-access & full-scans: "Detect Possibly Unwanted Applications." | `true` |
| `clamav__scan_max_directory_recursion` | "Maximum depth directories are scanned at." | `20` |
| `clamav__scan_max_file_size` | Full-scan: "Files larger than this limit won't be scanned." | `'450M'` |
| `clamav__scan_max_recursion` | Specifies how deeply nested archives should be scanned recursively. | `30` |
| `clamav__scan_max_scan_size` | "Sets the maximum amount of data to be scanned for each input file." | `'450M'` |
| `clamav__scan_on_access_exclude_paths` | On-access: "Set the exclude paths. All subdirectories are also excluded." | `[]` |
| `clamav__scan_on_access_include_paths` | On-access: "Set the include paths (all files inside them will be scanned)." | `[]` |
| `clamav__scan_on_access_max_file_size` | On-access: "Don't scan files larger than this." | `'500M'` |
| `clamav__scan_on_access_prevention` | On-access: Prevents access to the file if a virus is found. Note that this also blocks the full-scan from accessing the files. | `false` |
| `clamav__whitelist_files` | Whitelist specific files. Use `sigtool --md5 my-false-positive-file` to generate the entry. Have a look at the [official documentation](https://docs.clamav.net/manual/Signatures/AllowLists.html#file-allow-lists) for details. | `[]` |
| `clamav__whitelist_signatures` | Whitelist specific signatures. Note that it is possible that one needs to whitelist multiple signatures for the same finding, as it can come from different databases with different names. Have a look at the example below and the [official documentation](https://docs.clamav.net/manual/Signatures/AllowLists.html#signature-ignore-lists) for details. | `[]` |


Example:
```yaml
# optional
clamav__clamd_service_enabled: true
clamav__clamdscan_on_calendar: '*-*-* 21:{{ 59 | random(seed=inventory_hostname) }}'
clamav__clamdscan_paths: '{{ clamav__scan_on_access_include_paths }}'
clamav__clamdscan_timer_enabled: false
clamav__clamonacc_service_enabled: false
clamav__freshclam_private_mirror: []
clamav__freshclam_service_enabled: true
clamav__mail_from: '{{ mailto_root__from }}'
clamav__mail_recipients: '{{ mailto_root__to }}'
clamav__mail_subject_prefix: '000-my-customer-'
clamav__scan_alert_broken_executables: true
clamav__scan_detect_pua: true
clamav__scan_max_directory_recursion: 20
clamav__scan_max_file_size: '450M'
clamav__scan_max_recursion: 30
clamav__scan_max_scan_size: '450M'
clamav__scan_on_access_exclude_paths:
  - '/root/private-files'
clamav__scan_on_access_include_paths:
  - '/root'
clamav__scan_on_access_max_file_size: '500M'
clamav__scan_on_access_prevention: false
clamav__whitelist_files:
  - '44d88612fea8a8f36de82e1278abb02f:68:eicar.com'
clamav__whitelist_signatures:
  - 'Eicar-Signature'
  - 'Eicar-Test-Signature'
  - 'Win.Test.EICAR_HDB-1'
  - 'Win.Test.EICAR_HSB-1'
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
