linuxfabrik.lfops.repo_epel
===========================

This role deploys the `Extra Packages for Enterprise Linux (EPEL) Repository <https://docs.fedoraproject.org/en-US/epel/>`_.

Tested on

* RHEL 7 (and compatible)
* RHEL 8 (and compatible)


Requirements
------------


Mandatory
~~~~~~~~~

This role does not have any mandatory requirements.


Optional
~~~~~~~~

This role does not have any optional requirements.


Tags
----

.. csv-table::
    :header-rows: 1

    Tag,                       What it does
    repo_epel,                 "Deploy the EPEL Repository"


Role Variables
--------------

Have a look at the ``main/defaults.yml`` for the variable defaults.


Mandatory
~~~~~~~~~

This role does not have any mandatory variables.


Optional
~~~~~~~~

repo_epel__mirror_url
^^^^^^^^^^^^^^^^^^^^^^

Set the URL to a custom mirror server providing the repository. Defaults to ``lfops__repo_mirror_url`` to allow easily setting the same URL for all ``repo_*`` roles, or else to ``''``.

Default:

.. code-block:: yaml

    repo_epel__mirror_url: '{{ lfops__repo_mirror_url | default("") }}'


License
-------

The Unlicense, see `LICENSE file <https://unlicense.org/>`_.


Author Information
------------------

`Linuxfabrik GmbH, Zurich <https://www.linuxfabrik.ch>`_
