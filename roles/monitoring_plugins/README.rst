linuxfabrik.lfops.monitoring_plugins
====================================

This role deploys the `Linuxfabik Monitoring Plugins <https://github.com/Linuxfabrik/monitoring-plugins>`_ and the corresponding `Plugin Library <https://github.com/Linuxfabrik/monitoring-plugins>`_ to ``/usr/lib64/nagios/plugins/`` and ``/usr/lib64/nagios/plugins/lib`` respectively, allowing them to be easily executed by a monitoring system.

Tested on

* RHEL 7 (and compatible)
* RHEL 8 (and compatible)
* Debian 9
* Debian 10
* Fedora
* Windows
* Suse

Additionally, this role allows you to deploy custom plugins which are placed under ``../host_files/{{ inventory_hostname }}/usr/lib64/nagios/plugins`` on the ansible host.


Requirements
------------

Mandatory:

* On RHEL-compatible systems, enable the EPEL repository (e.g. use the ``linuxfabrik.lfops.repo_epel`` role).
* python2 (including the ``python2-psutil`` module)

These requirements can also manually be fulfilled for RHEL 7/8 using:

.. code-block:: bash

    yum -y install epel-release
    yum -y install python2 python2-psutil

Optional:

* Have a look at the individual requirements of each check.


Tags
----

.. csv-table::
    :header-rows: 1

    Tag,                                What it does
    monitoring_plugins,                 "Deploy the monitoring plugins, including custom plugins"
    monitoring_plugins::custom,         "Only deploy the custom plugins"
    monitoring_plugins::nuitka_compile, "Windows only. Compile the python plugins using nuitka"


Role Variables
--------------

* Have a look at the ``main/defaults.yml`` for the variable defaults.

Mandatory
~~~~~~~~~

This role does not have any mandatory variables.

Optional
~~~~~~~~

monitoring_plugins__python_version
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

For which python version should the monitoring plugins be deployed? Possible options:

* ``2``: For python2
* ``3``: For python3

Default:

.. code-block:: yaml

    monitoring_plugins__python_version: 3


monitoring_plugins__repo_version
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Which version of the monitoring plugins should be deployed? Possible options:

* ``latest``: The latest release. See the `Releases <https://github.com/Linuxfabrik/monitoring-plugins/releases>`_.
* ``main``: The development version. Use with care.
* A specific release, for example ``2022030201``. See the `Releases <https://github.com/Linuxfabrik/monitoring-plugins/releases>`_.

Default:

.. code-block:: yaml

    monitoring_plugins__repo_version: 'latest'


monitoring_plugins__windows_variant
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Windows only.

Which variant of the monitoring plugins should be deployed? Possible options:

* ``nuitka``: Deploy the nuitka-compiled checks. This does not require python on the system.
* ``python``: Deploy the plain python. This requires python on the system.

Default:

.. code-block:: yaml

    monitoring_plugins__windows_variant: 'nuitka'


monitoring_plugins__plugin_list
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Overwrite the automatically generated list of monitoring plugins that should be deployed.

Default: unset

Example:

.. code-block:: yaml

    monitoring_plugins__plugin_list:
      - 'about-me'
      - 'cpu-usage'


Examples
--------

Install or update just the ``php-version`` check plugin from the ``develop`` branch to/on server ``test01`` in ``mynet``:

.. code-block:: bash

    ansible-playbook \
        linuxfabrik.lfops.monitoring_plugins \
        --inventory environments/mynet/inventory \
        --extra-vars='{"monitoring_plugins": ["php-version"]}' \
        --limit test01


License
-------

The Unlicense, see `LICENSE file <https://unlicense.org/>`_.


Author Information
------------------

`Linuxfabrik GmbH, Zurich <https://www.linuxfabrik.ch>`_
