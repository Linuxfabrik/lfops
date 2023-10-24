Linuxfabrik's Ansible Development Guidelines
============================================

Rules of Thumb
--------------

Playbooks:

* Each playbook must contain all dependencies to run flawlessly against a newly installed machine.
* Playbooks installing an application together with software packages that are complex to configure (``apache_httpd``, ``mariadb_server`` and/or ``php``) as a dependency are prefixed by ``setup_``. Example: ``setup_nextcloud`` because Nextcloud also needs Apache httpd, MariaDB Server etc.
* After creating a new playbook, add it in the ``playbooks/all.yml``.

Roles:

* To understand/use a role, reading the readme and the defaults/main.yml must be enough.
* Idempotency: Roles should not perform changes when applied a second time to the same system with the same parameters, and it should not report that changes have been done if they have not been done. More importantly, it should not damage an existing installation when applied a second time (even without tags). Example:

    .. code-block:: yaml

          - name: Create new DBA '{{ mariadb_root.user }}' after a fresh installation
            ansible.builtin.command: mysql --unbuffered --execute '{{ item }}'
            with_items:
              - create user if not exists "{{ mariadb_root.user }}"@"%" identified by "{{ mariadb_root.password }}";
              - grant all privileges on *.* to "{{ mariadb_root.user }}"@"%" with grant option;
              - flush privileges;
            register: mariadb_new_dba_result
            changed_when: mariadb_new_dba_result.stderr is not match('ERROR \d+ \(28000\).*')
            failed_when: mariadb_new_dba_result.rc != 0 and mariadb_new_dba_result.stderr is not match('ERROR \d+ \(28000\).*')

* If a role was run without tags, it should deliver a completely installed application (assuming it installs an application).
* Do not over-engineer the role during the development - it should fulfill its use case, but can grow and be improved on later.
* The role should support the installation and configuration of multiple major versions of the software. For example, PHP 7.1, 7.2, 7.3 etc. should all be supported by a single role. Upgrades are either done manually or using Ansible, depending on the software and the implementation effort.
* Do not use role dependencies via ``meta/main.yml``. Dependencies make it harder to maintain a role, especially if it has many complex dependencies.
* Whenever the role requires a list as an input, use a list of dictionaries, preferably with `state: present/absent`. See "Injections" below.

Common:

* Document all changes in the `CHANGELOG.md <https://github.com/Linuxfabrik/lfops/blob/main/CHANGELOG.md>`_ file.
* Do not support and remove software versions that are EOL.


Pre-Commit
----------

We are using `pre-commit <https://pre-commit.com/>`_ to make sure any changes adhere to the styling rules. Install `pre-commit <https://pre-commit.com/#install>`_, then configure it as a git-hook using: ``pre-commit install``.


Style Guide
-----------

* Do not use ``---`` at the top of YAML files. It is only required if one specifies YAML directives above it.
* For YAML files, use the ``.yml`` extension. This is consistent with ``ansible-galaxy init``.
* In YAML files, use 2 spaces for indentation. Elsewhere prefer 4 spaces.
* Do not use special characters other than underscores in variable names.
* Try to name tasks after their respective shell commands. Exceptions are STIG tasks (they are too small, and too many to achieve a consistent naming).
* Split long Jinja2 expressions into multiple lines.
* Use the ``| bool`` filter when using bare variables (expressions consisting of just one variable reference without any operator).
* Use ``true`` / ``false`` instead of ``yes`` / ``no``, as they are actually part of YAML.
* Indent list items:

    Do:

    .. code-block:: yaml

        list1:
          - item1
          - item2

    Don't:

    .. code-block:: yaml

        list2:
        - item1
        - item2
        list3: [ 'tag1', 'tag2' ]

* Use RFC `5737 <https://datatracker.ietf.org/doc/html/rfc5737>`_, `3849 <https://datatracker.ietf.org/doc/html/rfc3849>`_, `7042 <https://datatracker.ietf.org/doc/html/rfc7042#section-2.1.1>`_ and `2606 <https://datatracker.ietf.org/doc/html/rfc2606>`_ in examples / documentation:

    * IPv4 Addresses: ``192.0.2.0/24``, ``198.51.100.0/24``, ``203.0.113.0/24``
    * IPv6 Addresses: ``2001:DB8::/32``
    * MAC Addresses: ``00-00-5E-00-53-00 through 00-00-5E-00-53-FF`` (unicast), ``01-00-5E-90-10-00 through 01-00-5E-90-10-FF`` (multicast)
    * Domains: ``*.example``, ``example.com``


Quotes
------

* We always quote strings and prefer single quotes over double quotes. The only time you should use double quotes is when they are nested within single quotes (e.g. Jinja map reference), or when your string requires escaping characters (e.g. using ``\n`` to represent a newline).
* If you must write a long string, we use the "folded scalar" (``>`` converts newlines to spaces, ``|`` keeps newlines) style and omit all special quoting.
* Do not quote booleans (e.g. ``true``/``false``).
* Do not quote numbers (e.g. ``42``).
* Do not quote octal numbers (e.g. ``0755``).
* Do not quote things referencing the local Ansible environment (e.g. boolean logic in ``when:` statements or names of variables we are assigning values to).

.. code-block:: yml

    # bad
    - name: start robot named S1m0ne
      service:
        name: s1m0ne
        state: started
        enabled: true
      become: yes

    # good
    - name: 'start robot named S1m0ne'
      ansible.builtin.service:
        name: 's1m0ne'
        state: 'started'
        enabled: true
      become: true

    # double quotes w/ nested single quotes
    - name: 'start all robots'
      ansible.builtin.service:
        name: '{{ item["robot_name"] }}'
        state: 'started'
        enabled: true
      with_items: '{{ robots }}'
      become: true

    # double quotes to escape characters
    - name 'print some text on two lines'
      ansible.builtin.debug:
        msg: "This text is on\ntwo lines"

    # folded scalar style
    - name: 'robot infos'
      ansible.builtin.debug:
        msg: >
          Robot {{ item['robot_name'] }} is {{ item['status'] }} and in {{ item['az'] }}
          availability zone with a {{ item['curiosity_quotient'] }} curiosity quotient.
      with_items: robots

    # folded scalar when the string has nested quotes already
    - name: 'print some text'
      ansible.builtin.debug:
        msg: >
          "I haven’t the slightest idea," said the Hatter.

    # don't quote booleans/numbers
    - name: 'download google homepage'
      ansible.builtin.get_url:
        dest: '/tmp'
        timeout: 60
        url: 'https://google.com'
        validate_certs: true

    # variables example 1
    - name: 'set a variable'
      ansible.builtin.set_fact:
        my_var: 'test'

    # variables example 2
    - name: 'print my_var'
      ansible.builtin.debug:
        var: my_var
      when: ansible_facts['os_family'] == 'Darwin'

    # variables example 3
    - name: 'set another variable'
      ansible.builtin.set_fact:
        my_second_var: '{{ my_var }}'

Why?

Even though strings are the default type for YAML, syntax highlighting looks better when explicitly set types. This also helps troubleshoot malformed strings when they should be properly escaped to have the desired effect.


Whitespace-Control in Jinja-Templates
-------------------------------------

So called "Block Scalar Styles":

* ``>``: Folded. Single line breaks within the string are replaced by a space. All trailing line breaks except one are removed.
* ``|``: Literal. Preserves every line break in the string. All trailing line breaks except one are removed.
* ``>-``, ``|-``: Strip the final line break and any trailing empty lines.
* ``>+``, ``|+``: Keep the final line break and any trailing empty lines.

Any indention remains only for the first line of a multiline variable content.

Insert whitespaces around Jinja filters like so: ``{{ my_var | d("my_default") }}``.

See also:

* https://yaml.org/spec/1.2.2/
* https://jinja.palletsprojects.com/en/latest/templates/#whitespace-control



Deploying files to the remote server
------------------------------------

* Always use the ``ansible.builtin.template`` module instead of the ``ansible.builtin.copy`` module, even if there are currently no variables in the file. This makes it easier to extend later on, and allows the usage of an automatically generated header.

* Always add the following to the top of templates, using the appropriate comment syntax:

    .. code-block::

        # {{ ansible_managed }}
        # 2021081601

* Do not use ``{{ template_run_date }}``. Such a timestamp is the date of the last change to the template itself, but changes on every Ansible run.

* Use the target path for the file in the ``template`` folder, for example: ``templates/etc/httpd/sites-available/default.conf.j2``. This makes it clear what the file is for, and avoids name collisions.

* Always use the ``.j2`` file extension for files in the ``template`` folder.

* If deploying self-written scripts, copy them to ``/usr/local/bin`` (due to SELinux).


Handlers
--------

* Use handlers in favor to ``some_result is changed`` if no ``meta: flush_handlers`` is required or if it would prevent duplicate code.
* Since handlers are global, prefix them with the role name to make sure the correct one is used.


Modules
-------

* Always use meta modules wherever possible:

    * ``ansible.builtin.package`` instead of ``ansible.builtin.yum``, ``ansible.builtin.dnf`` or ``ansible.builtin.apt``
    * ``ansible.builtin.service`` instead of ``ansible.builtin.systemd``

* Use some modules in preference to others:

    * ``ansible.builtin.command`` or ``ansible.windows.win_command`` over ``ansible.builtin.shell`` over ``ansible.builtin.raw``
    * ``ansible.builtin.template`` over ``ansible.builtin.copy`` if deploying files to the remote host (see above)

* Always use ``state: 'present'`` for the ``ansible.builtin.package`` module - we are installing, not updating.
* Always use the FQCN of the module.
* ``ansible.builtin.uri`` module: if consuming a RESTful API, check if it is returning the required content

    .. code-block:: yaml

        tasks:
          - ansible.builtin.uri:
              url: 'http://api.example.com'
              return_content: yes
            register: apiresponse
          - fail:
              msg: 'version was not provided'
            when: "version" not in apiresponse.content


Tags
----

* Naming scheme: ``role_name`` and ``role_name:section``, for example ``apache_httpd``, ``apache_httpd:vhosts``.
* The role should only do what one expects from the tag name. For example, the ``mariadb:user`` tag only manages MariaDB users.
* The README of a role should provide a list of the available tags and what they do.
* The tags should be set in the role itself. Do not set them in the playbook.
* Blocks/tasks that install base packages do not need a tag like ``apache:pkgs``, ``apache:setup`` or ``apache:install``. Why? There is no reason to just run the setup task by tag, you always need to do at least some configuration afterwards.
* For each task, consider to which areas it belongs. A task will usually have multiple tags.


Being OS-specific
-----------------

OS-specific Tasks
~~~~~~~~~~~~~~~~~

To indicate on which operating system platforms the role can be used, (empty) files must be placed in ``tasks/`` which have the file name of the supported "os family". In these files you probably want to perform platform specific tasks once, for the most specific match.

Assume you have the following OS-specific task files, in order of most specific to least specific:

* ``tasks/CentOS7.4.yml``
* ``tasks/CentOS7.yml``
* ``tasks/RedHat.yml``
* ``tasks/main.yml``

Now, if you run Ansible against a *CentOS 7.9* host, for example, only these tasks are processed in the following order:

1. ``tasks/CentOS7.yml``
2. ``tasks/main.yml``

Include the OS-specific tasks in the ``tasks/main.yml`` like this, and set the tags appropriately (should contain all tags of the possibly included task files):

.. code-block:: yaml

    - name: 'Perform platform/version specific tasks'
      ansible.builtin.include_tasks: '{{ lookup("first_found", __task_file) }}'
      vars:
        __task_file:
          files:
            - '{{ ansible_facts["distribution"] }}{{ ansible_facts["distribution_version"] }}.yml'
            - '{{ ansible_facts["distribution"] }}{{ ansible_facts["distribution_major_version"] }}.yml'
            - '{{ ansible_facts["distribution"] }}.yml'
            - '{{ ansible_facts["os_family"] }}{{ ansible_facts["distribution_version"] }}.yml'
            - '{{ ansible_facts["os_family"] }}{{ ansible_facts["distribution_major_version"] }}.yml'
            - '{{ ansible_facts["os_family"] }}.yml'
          paths:
            - '{{ role_path }}/tasks'
      tags:
        - 'role'
        - 'role:tag1' # for example, this tag could only be present in RedHat.yml

Make sure to set the tags directly on the `include_tasks` task, and not on a surrounding block. Setting it on a block causes the tag to be inherited to all tasks in that block, therefore also to included tasks. See the following example for details:

.. code-block:: yaml

    # RedHat.yml
    - block:

      - name: 'task 1'
        ansible.builtin.debug:
          msg: 'task 1 {{ test__var1 }}'

      tags:
        - 'test'
        - 'test:one'


    - block:

      - name: 'task 2'
        ansible.builtin.debug:
          msg: 'task 2 {{ test__var2 }}'

      tags:
        - 'test'


    # main.yml
    # THIS WORKS:
    - name: 'Perform platform/version specific tasks'
      ansible.builtin.include_tasks: 'RedHat.yml'
      tags:
        - 'test'
        - 'test:one'

    # without tags, whole playbook:
    # task 1 one
    # task 2 two

    # --tags test
    # task 1 one
    # task 2 two

    # --tags test:one
    # task 1 one

    # --tags other
    # no debug output, and include_tasks is not running


    # THIS DOES NOT WORK:
    - block:

      - name: 'Perform platform/version specific tasks'
        ansible.builtin.include_tasks: 'RedHat.yml'

      tags:
        - 'test'
        - 'test:one'

    # without tags, whole playbook:
    # task 1 one
    # task 2 two

    # --tags test
    # task 1 one
    # task 2 two

    # --tags test:one
    # task 1 one
    # task 2 two # we don't want this task to run

    # --tags other
    # no debug output, and include_tasks is not running


OS-specific Variables
---------------------

You normally use ``vars/main.yml`` (automatically included) to set variables used by your role. If some variables need to be parameterized according to distribution and version (name of packages, configuration file paths, names of services), use OS-specific vars-files.

Variables with the same name are overridden by the files in ``vars/`` in order from least specific to most specific:

* ``os_family`` covers a group of closely related platforms (e.g. ``RedHat`` covers ``RHEL``, ``CentOS``, ``Fedora``)
* ``distribution`` (e.g. ``CentOS``) is more specific than os_family
* ``distribution_major_version`` (e.g. ``CentOS7``) is more specific than distribution
* ``distribution_version`` (e.g. ``CentOS7.9``) is the most specific

As always be aware of the fact that dicts and lists are completely replaced, not merged.

Include the ``platform-variables.yml`` in the ``tasks/main.yml`` like this, and set the tags appropriately (should contain all tags tasks that could require the variables):

.. code-block:: yaml

    - name: 'Set platform/version specific variables'
      ansible.builtin.import_role:
        name: 'shared'
        tasks_from: 'platform-variables.yml'
      tags:
        - 'role'
        - 'role:tag1' # for example, tag for a task which requires a platform specific varialbe

For this task, it does not matter if the tags are set directly on the task itself or on a surrounding block.


OS-specific Filenames
~~~~~~~~~~~~~~~~~~~~~

For example:

* AIX.yml
* Amazon.yml
* Archlinux.yml
* CentOS.yml
* CentOS6.yml
* CentOS7.yml
* CentOS7.3.yml
* Container Linux by CoreOS.yml
* Debian.yml
* Debian11.yml
* Fedora.yml
* Fedora33.yml
* FreeBSD.yml
* Gentoo.yml
* OpenBSD.yml
* openSUSE Leap15.yml
* RedHat.yml
* RedHat8.yml
* RedHat8.2.yml
* Suse.yml
* Ubuntu.yml
* Ubuntu20.yml


Variables
---------

* ``./vars``: Variables that are not to be edited by users
* ``./defaults``: Default variables for the role, might be overridden by the user using group_vars or host_vars
* Naming scheme: ``<role name>__<optional: config file>_<setting name>``, for example ``apache_httpd__server_admin``.
* Every argument accepted from outside of the role should be given a default value in ``defaults/main.yml``. This allows a single place for users to look to see what inputs are expected. Avoid giving default values in vars/main.yml as such values are very high in the precedence order and are difficult for users and consumers of a role to override.
* No need to invent new names, use the key-names from the config file (if possible), for example ``redis__conf_maxmemory``.
* Avoid embedding large lists or "magic values" directly into the playbook. Such static lists should be placed into the ``vars/main.yml`` file and named appropriately.
* If you need random but predictable/idempotent values, use the ``inventory_hostname`` as seed. Example for setting the minutes of an hour: ``{{ 59 | random(seed=inventory_hostname) }}``
* Any secrets (passwords, tokens etc.) should not be provided with default values in the role. The tasks should be implemented in such a way that any secrets required, but not provided, should result in task execution failure. It is important for a secure-by-default implementation to ensure that an environment is not vulnerable due to the production use of default secrets. Deployers must be forced to properly provide their own secret variable values. Example:

    .. code-block:: yaml

        assert:
          that:
            - 'stig__grub2_password is defined'
            - 'stig__grub2_password | length'
          quiet: true
          fail_msg: 'Please define bootloader passwords for your hosts ("stig__grub2_password").''


Injections
~~~~~~~~~~

The goal of injections is that variables can be set in multiple places, and then merged in order to be used in the role.
For example, the user can overwrite a specific configuration role default (``__role_var``) from their inventory (``__host_var`` / ``__group_var``).

Furthermore, other roles can also inject their sensible defaults via the ``__dependent_var``, with a higher precedence than the role defaults, but lower than the user's inventory.

To enable this behaviour, one needs to define the ``__combined_var`` as follows:

.. code-block:: yaml

    # for list of dictionaries
    my_role__my_var__dependent_var: []
    my_role__my_var__group_var: []
    my_role__my_var__host_var: []
    my_role__my_var__role_var: []
    my_role__my_var__combined_var: '{{ (
          my_role__my_var__role_var +
          my_role__my_var__dependent_var +
          my_role__my_var__group_var +
          my_role__my_var__host_var
        ) | linuxfabrik.lfops.combine_lod
      }}'

    # for simple values like strings, numbers or booleans
    my_role__my_var__dependent_var: ''
    my_role__my_var__group_var: ''
    my_role__my_var__host_var: ''
    my_role__my_var__role_var: ''
    my_role__my_var__combined_var: '{{
        my_role__my_var__host_var if (my_role__my_var__host_var | string | length) else
        my_role__my_var__group_var if (my_role__my_var__group_var | string | length) else
        my_role__my_var__dependent_var if (my_role__my_var__dependent_var | string | length) else
        my_role__my_var__role_var
      }}'

The ``__combined_var`` will then be used in the tasks or templates of the role.

The role always has to implement some sort of ``state`` key, else the user cannot "unselect" a value defined in the defaults. Imagine the user wants to disable the default localhost vHost of the Apache HTTPd role:

.. code-block:: yaml

    # defaults/main.yml
    apache_httpd__vhosts__role_var:

      - conf_server_name: 'localhost'
        virtualhost_port: 80
        template: 'localhost'

Without the `state` key, the user has no way of achieving this, as they cannot remove previously defined elements from the list via the inventory. With the ``state`` key

.. code-block:: yaml

    # inventory
    apache_httpd__vhosts__role_var:

      - conf_server_name: 'localhost'
        virtualhost_port: 80
        state: 'absent'

will remove the vHost.

The handling of the state in the role can look something like this, assuming the default value for ``state`` is ``present``:

.. code-block:: yaml

    - name: 'Remove sites-available vHosts'
      ansible.builtin.file:
        path: '...'
        state: 'absent'
      when:
        - 'item["state"] | d("present") == "absent"'
      loop: '{{ apache_httpd__vhosts__combined_var }}'

    - name: 'Create sites-available vHosts'
      ansible.builtin.template:
        src: '...'
        dest: '...'
      when:
        - 'item["state"] | d("present") != "absent"'
      loop: '{{ apache_httpd__vhosts__combined_var }}'

Other times it is useful to generate a list of present and absent elements, for example when using ``ansible.builtin.package``, as providing the packages as a list is much faster than looping through them.

.. code-block:: yaml

    - name: 'Ensure PHP modules are absent'
      ansible.builtin.package:
        name: '{{ php__modules__combined_var | selectattr("state", "defined") | selectattr("state", "eq", "absent") | map(attribute="name") }}'
        state: 'absent'

    - name: 'Ensure PHP modules are present'
      ansible.builtin.package:
        name: '{{ (php__modules__combined_var | selectattr("state", "defined") | selectattr("state", "ne", "absent") | map(attribute="name"))
            + (php__modules__combined_var | selectattr("state", "undefined") | map(attribute="name")) }}'
        state: 'present'

Or in a Jinja2 template:

.. code-block::

    {% for role in apache_tomcat__roles__combined_var if role['state'] | d('present') != 'absent' %}
    <role rolename="{{ role['name'] }}"/>
    {% endfor %}

The vHost example above can be used to demonstrate another feature of ``linuxfabrik.lfops.combine_lod``. Normally, the list items are combined based on a ``unique_key`` that should match, for example, the ``name`` key. However, this does not work with ``conf_server_name`` because you can have a vHost with the same ``conf_server_name`` for multiple ports. This means that the ``unique_key`` must be a *combination* of ``conf_server_name`` and ``virtualhost_port``.:

.. code-block:: yaml

    apache_httpd__vhosts__combined_var: '{{ (
          apache_httpd__vhosts__role_var +
          apache_httpd__vhosts__dependent_var +
          apache_httpd__vhosts__group_var +
          apache_httpd__vhosts__host_var
        ) | linuxfabrik.lfops.combine_lod(unique_key=["conf_server_name", "virtualhost_port"])
      }}'

When setting a ``dependent_var`` in a playbook, make sure to use the following format to avoid needing to flatten the list:

.. code-block:: yaml

    - role: 'linuxfabrik.lfops.icinga2_master'
      icinga2_master__api_users__dependent_var: '{{
          icingadb__icinga2_master__api_users__dependent_var +
          icingaweb2__icinga2_master__api_users__dependent_var +
          icingaweb2_module_director__icinga2_master__api_users__dependent_var
        }}'

Note:

* Have a look at ``ansible-doc --type filter linuxfabrik.lfops.combine_lod``.
* Always use lists of dictionaries or simple values. Never use dictionaries, even though they allow overwriting of earlier elemens, since one cannot template the keyname using Jinja2. This would prevent passing on of variables, especially in `__dependent_var`` (for details have a look at https://docs.linuxfabrik.ch/software/ansible.html#besonderheiten-von-ansible).
* Simple value ``__combined_var`` are always returned as strings. Convert them to integers when using maths.


Ansible Facts / Magic Vars
~~~~~~~~~~~~~~~~~~~~~~~~~~

* Always use ``ansible_facts``. Currently, Ansible recognizes both the new fact naming system (using ``ansible_facts``) and the old pre-2.5 "facts injected as separate variables" naming system. The old naming system will be deprecated in a future release of Ansible.


Documenting Variables
~~~~~~~~~~~~~~~~~~~~~

* Document variables in the ``README``. Have a look at ``python_venv/README.md`` on how this could look like.


Handling default values
~~~~~~~~~~~~~~~~~~~~~~~

1. A Jinja template contains vendor defaults using ``{{ variable | d('vendor-default-value') }}``.
2. Is overridden by ``defaults/main.yml`` using Linuxfabrik's best practice value ``variable: linuxfabrik-default-value``.
3. May be overriden by the customer by using a ``group_vars`` or ``host_vars``  definition.


Git Commits
-----------

* Commit messages must start with "role:role_name: ", "plugin:plugin_name: ", or "module:module_name: " and clearly and precisely state what has changed. Example: ``role:duplicity: adjust name_email of gpg key to allow differentation``.
* If there is an issue, the commit message must consist of the issue title followed by "(fix #issueno)", for example: ``role:duplicity: adjust encryption to use a master gpg key (fix #12)``.
* For the first commit, use the message ``add <name>``.


Releases
--------

Releases are available on Ansible Galaxy. Changelogs have to be written according to https://keepachangelog.com/en/1.0.0/.


Special Roles
-------------

Roles with special technical implementations and capabilities:

* `librenms <https://github.com/Linuxfabrik/lfops/tree/main/roles/librenms>`_:

    * Compiles and loads an SELinux module.

* `nextcloud <https://github.com/Linuxfabrik/lfops/tree/main/roles/nextcloud>`_:

    * The role performs some tasks only on the very first run and never again after that. To do this, it creates a state file for itself so that it knows that it must skip certain tasks on subsequent runs.

* `php <https://github.com/Linuxfabrik/lfops/tree/main/roles/php>`_:

    * Build list for ansible.builtin.packages based on state ``present`` and ``absent``.
    * Some Jinja templates use non-default strings marking the beginning/end of a block.

* `redis <https://github.com/Linuxfabrik/lfops/tree/main/roles/redis>`_:

    * Gathers the installed version and deploys the corresponding config file.
    * Configures Systemd with Unit File overrides.

* `telegraf <https://github.com/Linuxfabrik/lfops/tree/main/roles/telegraf>`_:

    * Jinja templates use non-default strings marking the beginning/end of a print statement.

* `wordpress <https://github.com/Linuxfabrik/lfops/tree/main/roles/wordpress>`_:

    * chmod: Sets file and folder permissions separately using ``find``.


Credits
-------

* https://github.com/whitecloud/ansible-styleguide
* https://redhat-cop.github.io/automation-good-practices
* https://docs.openstack.org/openstack-ansible/latest/contributor/code-rules.html
