# Ansible Role linuxfabrik.lfops.rpm

This role checks that the RPM database can be read, before any package task depends on it. A damaged database otherwise makes the first package task of a later role abort with `rpmdb open failed` and no hint at the cause. The `setup_basic` playbook runs it first on every host; on Debian and Ubuntu, it does nothing.


*Available in the next LFOps release.*


## How the Role Behaves

* The role runs `rpm --verifydb` and `rpm --query rpm`, which only read the database, also in check mode. While another rpm or dnf transaction runs, it waits for up to 5 minutes. For the moment `rpm --verifydb` holds the transaction lock, an rpm or dnf transaction started outside a terminal, for example by dnf-automatic, fails with `can't create transaction lock` and has to run again.
* If `rpm --verifydb` finds a damaged file, the run aborts. The role never runs `rpm --rebuilddb`, since that drops the packages it cannot read from the database without an error, see "Troubleshooting".
* If the files are intact but rpm still cannot open the database, as on RHEL 8 after an rpm process got killed (`DB_RUNRECOVERY: Fatal error, run database recovery`), the Berkeley DB environment in `/var/lib/rpm/__db.*` is broken. The role removes these files after checking that no process uses them, as Red Hat's [solution 6903](https://access.redhat.com/solutions/6903) describes, and rpm creates them again on its next call, with all packages kept. If a process still uses them, the run aborts and names the process instead.


## Tags

`rpm`

* Checks the RPM database and, on RHEL 8, removes a broken Berkeley DB environment.
* Triggers: none.


## Troubleshooting

**The run aborts with `rpm: The RPM database in /var/lib/rpm is damaged`**

* Copy the database directory before you change anything, for example `cp --archive /var/lib/rpm /root/rpmdb-backup` (on RHEL 10, the directory is `/usr/lib/sysimage/rpm`).
* Follow Red Hat's procedure: [How to rebuild RPM database on a Red Hat Enterprise Linux system?](https://access.redhat.com/solutions/6903) for RHEL 8, which rebuilds the `Packages` file with `rpmdb_dump` and `rpmdb_load` and then runs `rpm --rebuilddb`, and [SQLite RPM database in Red Hat Enterprise Linux 9 and later](https://access.redhat.com/articles/6891951), which runs `rpm --rebuilddb` or exports and imports the database with `rpmdb --exportdb` / `rpmdb --importdb`. Each of these steps drops the packages it cannot read without an error, and `rpm --verifydb` passes afterwards.
* Afterwards, compare `rpm --query --all` with the packages in `/var/log/dnf.rpm.log` or on a host installed the same way. Install the missing packages again with `dnf install`, or register them without touching their files with `rpm --install --justdb`, as Red Hat suggests. Import missing `gpg-pubkey` entries with `rpm --import`.

**The run aborts with `has held the RPM database ... for more than 5 minutes`**

* An rpm or dnf transaction is still running, for example a large update. Check it with `ps -C rpm,dnf,dnf-automatic,yum -o pid,etime,args`, and run the role again once it has finished.

**The run aborts with `these processes still use it`**

* Usually a dnf or rpm process that hangs. Check it with `ps -p <pid>`, end it, and run the role again. rpm postpones `SIGTERM` while it holds the database open, so a process that hangs may need `kill -KILL <pid>`.


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
