Compatibility
=============

Which Ansible role is proven to run on which OS?

.. csv-table::
    :header-rows: 1

    Role,                                   Debian 10,  Debian 11,  Debian 12,  RHEL 7, RHEL 8, RHEL 9, Ubuntu 16.04,   Ubuntu 18.04,   Ubuntu 20.04,   other
    acme_sh,                                ,           ,           ,           ,       x,      ,       ,               ,               ,               
    ansible_init,                           ,           ,           ,           ,       ,       ,       ,               ,               ,               Fedora 35+
    cockpit,                                ,           ,           ,           ,       x,      x,      x,              ,               ,               Fedora 35
    monitoring_plugins,                     x,          ,           ,           x,      x,      ,       x,              ,               ,               "Debian 9, Fedora, Suse, Windows"
    repo_mongodb,                           ,           x,          ,           ,       x,      x,      ,               ,               ,               


Legend:

* empty: don't know/unproven/untested
* "x": proven/works on this OS
