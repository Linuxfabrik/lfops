linuxfabrik.lfops.python_venv
=============================

This role creates and manages different `Python 3 virtual environments (venv) <https://docs.python.org/3/library/venv.html>`_. These are placed beneath ``/opt/python-venv/`` on the target system.

Tested on

* RHEL 7 (and compatible)
* RHEL 8 (and compatible)


Requirements
------------

Mandatory
~~~~~~~~~

* Install Python 3


Optional
~~~~~~~~

This role does not have any optional requirements.


Tags
----

.. csv-table::
    :header-rows: 1

    Tag,                       What it does
    python_venv,               "Creates and manages the virtual environments"


Role Variables
--------------

Have a look at the ``main/defaults.yml`` for the variable defaults.


Mandatory
~~~~~~~~~

This role does not have any mandatory variables.


Optional
~~~~~~~~

python_venv__host_venvs / python_venv__group_venvs
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

These variables are intended to be used in a host / group variable file in the Ansible inventory. Note that the group variable can only be used in one group at a time.

Dictionary containing definitions for the virtual environments.

Subkeys:

``name``
    Mandatory, string.
    The name of the virtual environment. Will be used for the folder name beneath ``/opt/python-venv``.

``packages``
    Mandatory, list.
    These packages will be installed in the virtual environment using ``pip``.

``system_site_packages``
    Optional, boolean. Defaults to ``True``.
    Give the virtual environment access to the system site-packages dir.

``package_requirements``
    Optional, list.
    These packages will be installed before installing the pip ``packages`` using the default package manager (e.g. ``dnf``).

``exposed_binaries``
    Optional, list.
    List of binaries which should be linked to ``/usr/local/bin`` for easier access on the command line. The binaries are expected to exist beneath ``/opt/python-venv/name/bin/``.

Default:

.. code-block:: yaml

    python_venv__host_venvs: []
    python_venv__group_venvs: []

Example:

.. code-block:: yaml

    python_venv__host_venvs:
      - name: 'duplicity'
        packages:
          - 'duplicity'
          - 'python-swiftclient'
          - 'python-keystoneclient'
        package_requirements:
          - 'gcc'
          - 'librsync-devel'
        exposed_binaries:
          - 'duplicity'

License
-------

The Unlicense, see `LICENSE file <https://unlicense.org/>`_.


Author Information
------------------

`Linuxfabrik GmbH, Zurich <https://www.linuxfabrik.ch>`_
