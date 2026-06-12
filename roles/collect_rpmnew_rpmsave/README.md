# Ansible Role linuxfabrik.lfops.collect_rpmnew_rpmsave

When an RPM-based system updates a package, RPM keeps the old config file and writes its new version with a `.rpmnew` suffix (when the user had modified the original) or saves the user's version as `.rpmsave` (when the new package replaces a previously customized file). Either way, somebody has to diff and reconcile the two files manually.

This role fetches every such pending file from the remote hosts back to the `/tmp/lfops` directory of the Ansible control node so the admin can review them centrally. Typically, you invoke the role like this:

```bash
for INV in {inventoy01,inventory02,inventory03}
do
    ansible-playbook --inventory=$INV linuxfabrik.lfops.collect_rpmnew_rpmsave
done
```

The role starts by locating all files with the extensions `*.rpmnew` and `*.rpmsave`. It then extracts the corresponding package name and version for each identified file, and maps each file to its specific package information. Once the mapping is complete, it downloads both the `*.rpmnew` and `*.rpmsave` files, along with their original counterparts, to the control node for further processing and archiving.

The resulting files are organized by `[distribution][distribution_major_version]__[rpm -qf filename]`. Example:

```
lfops
├── CentOS7__coolwsd-24.04.4.1-1.x86_64
│   └── srv01
│       └── etc
│           └── coolwsd
│               ├── coolwsd.xml
│               └── coolwsd.xml.rpmnew
├── Rocky8__coolwsd-24.04.4.2-1.x86_64
│   ├── srv26
│   │   └── etc
│   │       └── coolwsd
│   │           ├── coolwsd.xml
│   │           └── coolwsd.xml.rpmnew
│   ├── srv06
│   │   └── etc
│   │       └── coolwsd
│   │           ├── coolwsd.xml
│   │           └── coolwsd.xml.rpmnew
│   └── srv74
│       └── etc
│           └── coolwsd
│               ├── coolwsd.xml
│               └── coolwsd.xml.rpmnew
└── Rocky8__systemd-239-82.el8.x86_64
    └── srv74
        └── etc
            └── systemd
                ├── logind.conf
                └── logind.conf.rpmnew

```

The resulting set of files can then be further analyzed, for example by hand or using the `list-rpmnew-rpmsave` tool. This methodical approach helps to maintain system updates efficiently.


*Available since LFOps `3.0.0`.*


## Tags

`collect_rpmnew_rpmsave`

* Collect all rpmnew/rpmsave files.
* Triggers: none.


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
