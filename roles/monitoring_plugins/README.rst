linuxfabrik.lfops.monitoring_plugins
====================================

This role deploys the `Linuxfabik Monitoring Plugins <https://github.com/Linuxfabrik/monitoring-plugins>`_ to ``/usr/lib64/nagios/plugins/``, allowing them to be easily executed by a monitoring system.

Tested on

* RHEL 7 (and compatible)
* RHEL 8 (and compatible)
* Debian 9
* Debian 10
* Fedora
* Windows
* Suse

Additionally, this role allows you to deploy custom plugins which are placed under ``../host_files/{{ inventory_hostname }}/usr/lib64/nagios/plugins`` on the ansible host.

It also installs the `Linuxfabrik Plugin Library <https://github.com/Linuxfabrik/monitoring-plugins>`_ to ``/usr/lib64/nagios/plugins/lib``, a must have for all Monitoring Plugins.

What this role does **NOT** do:

* Install Python 3 (or Python 2 if needed)
* Install all other 3rd party libraries used by some of the Monitoring Plugins:

    * BeautifulSoup4
    * lxml
    * mysql.connector
    * psutil

* If on Windows and you want to compile the python plugins using Nuitka, you need of course Nuitka.


Requirements
------------

Prepare your target node as described in the `Monitoring-Plugins README <https://github.com/Linuxfabrik/monitoring-plugins>`_.


Tags
----

.. csv-table::
    :header-rows: 1

    Tag,                                What it does
    monitoring_plugins,                 "Deploy the monitoring plugins, including Linuxfabrik libraries and custom plugins"
    monitoring_plugins::custom,         "Only deploy the custom plugins"
    monitoring_plugins::nuitka_compile, "Windows only: Only compile the python plugins using nuitka"


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

* ``3``: For Python 3
* ``2``: For Python 2

Default:

.. code-block:: yaml

    monitoring_plugins__python_version: 3


monitoring_plugins__repo_version
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Which version of the monitoring plugins should be deployed? Possible options:

* ``latest``: The **latest stable** release. See the `Releases <https://github.com/Linuxfabrik/monitoring-plugins/releases>`_.
* ``main``: The development version. Use with care.
* A specific release, for example ``2022030201``. See the `Releases <https://github.com/Linuxfabrik/monitoring-plugins/releases>`_.

Default:

.. code-block:: yaml

    monitoring_plugins__repo_version: 'latest'


monitoring_plugins__windows_variant
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Windows only.

Which variant of the monitoring plugins should be deployed? Possible options:

* ``nuitka``: Deploy the nuitka-compiled checks (EXE files). This does not require python on the system.
* ``python``: Deploy the plain python checks. This requires Python to be installed on Windows.

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

Install or update just the ``php-version`` check plugin to/on server ``test01`` in ``mynet``, using the latest stable version:

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
