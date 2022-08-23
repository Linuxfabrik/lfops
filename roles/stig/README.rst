Secure Technical Implementation Guide  - Audit and Remediations
===============================================================

TODO

Overview
--------

Round about 300 unofficial audit and remediation tasks for different Secure Technical Implementation Guides (STIG).

Compiled STIGs:

.. csv-table::
    :header-rows: 1

    Type, Name,                             Version,  ``stig_profile_name:``,         ``stig_profile_version:``, Tested Platforms
    CIS,  Apache HTTP Server 2.4 Benchmark, v2.0.0,   ``CIS Apache HTTP Server 2.4``, ``v2.0.0``,                "RHEL 7+ compatible, Debian 10+ compatible"
    CIS,  CentOS Linux 7 Benchmark,         v3.1.2,   ``CIS CentOS Linux 7``,         ``v3.1.2``,                RHEL 7+ compatible
    CIS,  CentOS Linux 8 Benchmark,         v1.0.1,   ``CIS CentOS Linux 8``,         ``v1.0.1``,                RHEL 7+ compatible

`Drop us a line <https://www.linuxfabrik.ch/ueber-uns/kontakt>`_ if you have successfully used any of the STIG profiles on other platforms.

To audit before and after applying the remediations, you might use tools like `OpenVAS <https://www.openvas.org/>`_, `Lynis <https://cisofy.com/lynis/>`_, `Nessus <https://www.tenable.com>`_ or our Python script `files/audit.py <https://git.linuxfabrik.ch/linuxfabrik-ansible/roles/stig/-/blob/master/files/audit.py>`_. Remediations are done using the `tasks/main.yml <https://git.linuxfabrik.ch/linuxfabrik-ansible/roles/stig/-/blob/master/tasks/main.yml>`_.

.. attention::

    Do not attempt to use any of the Ansible tasks without first testing them in a non-operational environment. Linuxfabrik assume no responsibility whatsoever for its use by other parties, and makes no guarantees, expressed or implied, about its quality, reliability, or any other characteristic.

.. note::

    * This role cannot be run with the ``--check`` parameter.
    * Password-less SSH access is required for the audits and remediations.
    * "CentOS" also fits RHEL, Rocky Linux, AlmaLinux, Oracle Linux etc.


Before you begin
----------------

While remediating, this role breaks things on productive machines when applied completely.
    This role **will make changes to the system that could or will break things**. Please take the time to familarise yourself with the STIG profile of your choice before applying this role to a system.

Compile a list of non-applicable remediations for each server.
    For example: If you are running an outbound proxy with Squid and would like to apply the "CIS CentOS Linux 7 v3.1.2" profile, you should exclude "2.2.12 Ensure HTTP Proxy Server is not installed".

This role does not create or change host firewalls.
    Because there are far more firewall tools on earth than just firewalld, nftables and iptables, and maybe you create your firewall rules using other techniques or roles. This topic is too complex to be configured automatically.


Installation
------------

Place this Ansible role in an appropriate directory:

.. code-block:: text

    stig
    ├── defaults
    ├── files: Home of the audit.py Python script and of stig.db (SQLite database file)
    │   ├── audits: Contains all Audit Snippets (Bash)
    │   └── lib: Home of Linuxfabrik libraries
    ├── handlers
    ├── tasks: Contains a collection of remediation tasks used across various STIGs, for example CIS CentOS Linux 8.
    └── templates: Jinja templates for Ansible

If you want to use ``audit.py``:

* Install Python modules:

    .. code-block::

        dnf -y install python3-termcolor

* Copy all Python files from https://git.linuxfabrik.ch/linuxfabrik/lib into ``stig/files/lib``.


Auditing a Machine (audit.py)
-----------------------------

If using our Python script `files/audit.py <https://git.linuxfabrik.ch/linuxfabrik-ansible/roles/stig/-/blob/master/files/audit.py>`_, ensure that you are able to access the machine using SSH with root privileges and password-less authentication. Many audit scriptlets depend on ``sudo`` and ``curl``, so install them as well, otherwise you might get "None" as a result for many audits.

For example, start an audit only with controls whose name starts with "1", but at the same time exclude all controls whose name starts with "1.3" and "1.4":

.. code-block:: bash

    cd files
    ./audit.py --profile-name="CIS CentOS Linux 8" --hostname=192.0.2.249 --username=root --lengthy --control-name-include='^1' --control-name-exclude='^1\.3|1\.4'

Example output (parts ommitted)::

    Audit Result
    ============

    ...

    Summary Table
    -------------

    Control                                                                 ! Script            ! Scoring ! Lvl ! Result
    ------------------------------------------------------------------------+-------------------+---------+-----+-------
    1.1.1.1 Ensure mounting of cramfs filesystems is disabled (Automated)   ! cramfs-off.sh     ! Scored  ! 1   ! Failed
    1.1.1.2 Ensure mounting of squashfs filesystems is disabled (Automated) ! squashfs-off.sh   ! Scored  ! 2   ! Failed
    1.1.1.3 Ensure mounting of udf filesystems is disabled (Automated)      ! udf-off.sh        ! Scored  ! 1   ! Failed
    1.1.2 Ensure /tmp is configured (Automated)                             ! tmp-configure.sh  ! Scored  ! 1   ! Passed
    1.1.3 Ensure noexec option set on /tmp partition (Automated)            ! tmp-noexec-on.sh  ! Scored  ! 1   ! Passed
    1.1.4 Ensure nodev option set on /tmp partition (Automated)             ! tmp-nodev-on.sh   ! Scored  ! 1   ! Passed
    1.1.5 Ensure nosuid option set on /tmp partition (Automated)            ! tmp-nosuid-on.sh  ! Scored  ! 1   ! Passed
    ...

    Profile
    -------

    * Benchmark: CIS CentOS Linux 7 (v3.1.2)
    * Host:      ``192.0.2.194``
    * Datetime:  2021-09-28 14:22:45
    * Score:     128/236 points (54.2%)
    * Grade:     F

For each control:

* If you get a "Passed", the configuration is CIS-compliant for that control.
* If you get a "Failed", the the CIS requirements is not met.
* If you get the result "Review", it means we cannot automatically detect if the configuration is CIS-compliant or not. You have to check the configuration manually in that case.

The overall grade is calculated as follows:

.. code-block:: python

    def get_grade(percentage):
        if percentage >= 97:
            return 'A+'
        if percentage >= 93:
            return 'A'
        if percentage >= 90:
            return 'A-'
        if percentage >= 87:
            return 'B+'
        if percentage >= 83:
            return 'B'
        if percentage >= 80:
            return 'B-'
        if percentage >= 77:
            return 'C+'
        if percentage >= 73:
            return 'C'
        if percentage >= 70:
            return 'C-'
        if percentage >= 67:
            return 'D+'
        if percentage >= 63:
            return 'D'
        if percentage >= 60:
            return 'D-'
        return 'F'


Remediating a Machine
---------------------

We have implemented more audits than remediation measures, especially in the area of application servers (for example Apache). The reason: Audits are not only easier to implement, but the configuration of an existing application server is far too specialized and complex to be done by a small, general role. Better, specialized or custom Ansible roles must be used here to deploy and maintain the server.

After applying remediations:

* Reboot. Always reboot a remediated machine to be sure for all settings to take effect.
* Keep an eye on your monitoring software.
* Run a second audit.
* Fix further findings using other roles.

Variables (have a look at `defaults/main.yml <https://git.linuxfabrik.ch/linuxfabrik-ansible/roles/stig/-/blob/master/defaults/main.yml>`_ for a complete list of available variables):

.. code-block:: yml

    stig:
    - profile_name: 'CIS Apache HTTP Server 2.4'      # mandatory
      profile_version: 'v2.0.0'                       # default: "latest"
      also_use_controls_disabled_by_default: True     # default: false
      control_name_include:    # use regular expressions here
        - '^1'
        - '^2'
      control_name_exclude:    # use regular expressions here
        - '^2\.1'
        - '^2\.3'


Ansible Role Variables
----------------------

Have a look at `defaults/main.yml <https://git.linuxfabrik.ch/linuxfabrik-ansible/roles/stig/-/blob/master/defaults/main.yml>`_ for a complete list of available variables.


STIG "CIS Apache HTTP Server 2.4" - Details
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To audit Apache, you must install and enable Apache ``mod_info`` beforehand and make it available at ``http://localhost/server-info``, for example like this:

.. code-block:: text

    <VirtualHost 127.0.0.1:80>
        ServerName localhost
        ServerAlias 127.0.0.1
        <IfModule info_module>
            <Location "/server-info">
                SetHandler server-info
                Require local
            </Location>
        </IfModule>
    </VirtualHost>

This, of course, means that any control labeled  "Ensure the Info Module Is Disabled" or something similar will return "Failed".

Ansible can only poorly take corrective action on existing Apache servers due to the complexity of the configuration and the different operating systems, which is why only the simplest remediations are implemented. It is better to deploy an Apache via Ansible that implements Security-by-Design from the beginning.

Some remediations are disabled by default for various reasons - enable them only if needed:

* | Ensure Apache Is Installed From the Appropriate Binaries (or similar)
  | Reason: Should be installed by a specialized Ansible Role, which implements Security-by-Design.


STIG "CIS CentOS Linux X Benchmark" - Details
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Mandatory:

* You have to set the ``stig__grub2_password`` variable.

Some remediations are disabled by default for various reasons - enable them only if needed:

* | Audit system file permissions (or similar)
  | Reason: File permissions can be reset by the package manager or even a reboot at any time, which means that auditing tends to fail. For this reason, our audit task ignores some of the known files in ``var/log``.
* | Ensure audit logs are not automatically deleted (or similar)
  | Reason: No customer likes to have his machine stopped simply because the audit partition runs out of space, and the mass of cryptic audit logs cannot be checked anyway.
* | Ensure password expiration is 365 days or less (or similar)
  | Reason: May lock you and Ansible out.
* | Ensure rsyslog is configured to send logs to a remote log host (or similar)
  | Reason: This is more complex in reality than the CIS mediation suggests.
* | Ensure SSH root login is disabled (or similar)
  | Reason: May lock you and Ansible out.
* | Ensure updates, patches, and additional security software are installed (or similar)
  | Reason: Skipping this saves quite some time during the run. Also, there are other possible update strategies.


stig.db
-------

This is a SQLite file and can be viewed and edited with *DB Browser for SQLite*, for example.

The ``control`` table contains a list of all audit scripts (mostly shell scripts) and the corresponding remediation tasks (mostly Ansible tasks).

The ``profile`` table contains STIG definitions (currently some CIS benchmarks). The meaning of some of the columns:

* ``exec_order``: Execution order within the specific STIG profile.
* ``enabled``: Specifies whether a *remediation* should be applied automatically or not. Set to "0" if this causes problems or is unnecessary.

Use NULL to unset any value.

To get a complete list of disabled remediations, execute this SQL statement on ``stig.db``:

.. code-block:: text

    SELECT *
    FROM profile
    WHERE
        enabled = 0

Some audits and remediations in some STIG profiles might not be implemented for various reasons. As an example, to get a list, execute this SQL statement on ``stig.db``:

.. code-block:: text

    SELECT *
    FROM profile
    WHERE
        profile_name = "CIS CentOS Linux 7"
        and control_id ISNULL


Naming Scheme for Controls
--------------------------

From a remediation action point of view: ``<package or device>[-<section or detail>][-<section or detail>]-<action>``

* package or device: for example "httpd" or "tmp"
* section: for example "vhosts"
* action: a remediation action that should be done. One of

    * get:          fetch some information - for audit tasks that will never have a remediation counterpart
    * compare:      compare two or more items - for audit tasks that will never have a remediation counterpart

    * off:          disabling or configuring something to "off"
    * on:           enabling or configuring something to "on"
    * disable:      disabling a service
    * enable:       enabling a service

    * install:      install a package
    * update:       update a package or packages
    * remove:       uninstalling a package, deleting files and directories

    * chmod:        changing permissions using chmod
    * chown:        changing owner using chown

    * cron:         configuring cronjobs
    * timer:        configuring systemd timer
    * select:       set something from a list of choices
    * configure:    more or less complex configuration tasks
    * setup:        both installation and configuration


Examples
--------

Auditing a RHEL-based VM, excluding some Controls:

.. code-block:: bash

    cd roles/stig/files/
    ./audit.py --lengthy --profile-name='CIS CentOS Linux 8' --profile-version='v1.0.1' --hostname=192.0.2.194 --control-name-exclude='^1\.9|^3\.4\.|^4\.1\.2\.2|^4\.2\.1\.5|^5\.2\.10|^5\.3\.1|^5\.3\.2|^5\.3\.3|^5\.4\.2|^5\.5\.1\.1'

Apply the remedies of "CIS CentOS Linux 8" to a Rocky machine (use this as a starting point):

.. code-block:: text

    # hosts.yml
    cis_hosts:
      vars:
        ansible_become: True
      hosts:
        192.0.2.194:

.. code-block:: text

    # host_vars/192.0.2.194.yml
    stig__crypto_policy: 'FIPS'
    stig__grub2_password: 'BlueLake23'

.. code-block:: text

    # group_vars/cis_hosts.yml
    stig:
      - profile_name: 'CIS CentOS Linux 8'
        profile_version: 'v1.0.1'   # or "latest"
        also_use_controls_disabled_by_default: False
        control_name_include:    # use regular expressions here
          - '^1'
          - '^2'
          - '^3'
          - '^4'
          - '^5'
          - '^6'
        control_name_exclude:
          - '^1\.9'

.. code-block:: text

    # playbook.yml
    - hosts:
        - 'cis_hosts'
      roles:
        - role: 'stig'

.. code-block:: bash

    ansible-playbook --inventory=path/to/hosts.yml path/to/playbook.yml --extra-vars="ansible_ssh_user=root"
