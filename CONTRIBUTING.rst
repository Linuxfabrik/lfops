Linuxfabrik's Ansible Development Guidelines
============================================

Rules of Thumb
--------------

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
* Do not over-engineer the role during the development - it should fulfill its use case but can grow and be improved on later.
* The role should support the installation and configuration of multiple major versions of the software. For example, PHP 7.1, 7.2, 7.3 etc. should all be supported by a single role. Upgrades are either done manually or using Ansible, depending on the software and the implementation effort.


Style Guide
-----------

* Do not use ``---`` at the top of YAML files. It is only required if one specifies YAML directives above it.
* For YAML files, use the ``.yml`` extension. This is consistent with ``ansible-galaxy init``.
* In YAML files, use 2 spaces for indentation. Elsewhere prefer 4 spaces.
* Do not use special characters other than underscores in variable names.
* Try to name tasks after their respective shell commands. Exceptions are STIG tasks (they are too small, and too many to achieve a consistent naming).
* Split long Jinja2 expressions into multiple lines.
* Use the ``| bool`` filter when using bare variables (expressions consisting of just one variable reference without any operator).
* Use ``True`` / ``False`` instead of ``yes`` / ``no``, as they are actually part of YAML.
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

* | We always quote strings and prefer single quotes over double quotes. The only time you should use double quotes is when they are nested within single quotes (e.g. Jinja map reference), or when your string requires escaping characters (e.g. using ``\n`` to represent a newline).
* | If you must write a long string, we use the "folded scalar" (``>`` converts newlines to spaces, ``|`` keeps newlines) style and omit all special quoting.
* | The only things you should avoid quoting are booleans (e.g. ``true``/``false``), numbers (e.g. ``42``), and things referencing the local Ansible environment (e.g. boolean logic or names of variables we are assigning values to).

.. code-block:: yml

    # bad
    - name: start robot named S1m0ne
      ansible.builtin.service:
        name: s1m0ne
        state: started
        enabled: true
      become: true

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
        name: '{{ item["robot_name"] }}''
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
              url: http://api.myapp.com
              return_content: yes
            register: apiresponse
          - fail:
              msg: 'version was not provided'
            when: "'version' not in apiresponse.content"


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

* ``tasks/CentOS_7.4.yml``
* ``tasks/CentOS_7.yml``
* ``tasks/RedHat.yml``
* ``tasks/main.yml``

Now, if you run Ansible against a *CentOS 7.9* host, for example, only these tasks are processed by ``platform-tasks.yml`` in the following order :

1. ``tasks/CentOS_7.yml``
2. ``tasks/main.yml``


OS-specific Variables
---------------------

You normally use ``vars/main.yml`` (automatically included) to set variables used by your role. If some variables need to be parameterized according to distribution and version (name of packages, configuration file paths, names of services), use OS-specific vars-files.

Variables with the same name are overridden by the files in ``vars/`` in order from least specific to most specific:

* ``os_family`` covers a group of closely related platforms (e.g. ``RedHat`` covers ``RHEL``, ``CentOS``, ``Fedora``)
* ``distribution`` (e.g. ``CentOS``) is more specific than os_family
* ``distribution_major_version`` (e.g. ``CentOS_7``) is more specific than distribution
* ``distribution_version`` (e.g. ``CentOS_7.9``) is the most specific

As always be aware of the fact that dicts and lists are completely replaced, not merged.


OS-specific Filenames
~~~~~~~~~~~~~~~~~~~~~

For example:

* AIX.yml
* Amazon.yml
* Archlinux.yml
* CentOS.yml
* CentOS_6.yml
* CentOS_7.yml
* CentOS_7.3.yml
* Container Linux by CoreOS.yml
* Debian.yml
* Debian_11.yml
* Fedora.yml
* Fedora_33.yml
* FreeBSD.yml
* Gentoo.yml
* OpenBSD.yml
* openSUSE Leap_15.yml
* RedHat.yml
* RedHat_8.yml
* RedHat_8.2.yml
* Suse.yml
* Ubuntu.yml
* Ubuntu_20.yml


Variables
---------

* ``./vars``: Variables that are not to be edited by users
* ``./defaults``: Default variables for the role, might be overridden by the user using group_vars or host_vars
* Naming scheme: ``<role name>__<optional: config file>_<setting name>``, for example ``apache_httpd__server_admin``.
* Every argument accepted from outside of the role should be given a default value in ``defaults/main.yml``. This allows a single place for users to look to see what inputs are expected. Avoid giving default values in vars/main.yml as such values are very high in the precedence order and are difficult for users and consumers of a role to override.
* No need to invent new names, use the key-names from the config file (if possible), for example ``redis__maxmemory``.
* Avoid embedding large lists or "magic values" directly into the playbook. Such static lists should be placed into the ``vars/main.yml`` file and named appropriately.
* Any secrets (passwords, tokens etc.) should not be provided with default values in the role. The tasks should be implemented in such a way that any secrets required, but not provided, should result in task execution failure. It is important for a secure-by-default implementation to ensure that an environment is not vulnerable due to the production use of default secrets. Deployers must be forced to properly provide their own secret variable values. Example:

    .. code-block:: yaml

        assert:
          that:
            - stig__grub2_password is defined
            - stig__grub2_password|length
          quiet: true
          fail_msg: Please define bootloader passwords for your hosts ("stig__grub2_password").

* Your role might accept variable injection from another role. It depends on the context on how to implement that. Examples:

    .. code-block:: yaml

        - ansible.builtin.set_fact:
            apache_httpd__combined_modules: '{{ apache_httpd__role_modules
              | combine(apache_httpd__role_proxy_modules)
              | combine(apache_httpd__dependent_modules)
              | combine(apache_httpd__group_modules)
              | combine(apache_httpd__host_modules)
             }}'

        - ansible.builtin.set_fact:
            apache_httpd__combined_vhosts: '{{ apache_httpd__group_vhosts +
              apache_httpd__host_vhosts +
              apache_httpd__role_vhosts +
              apache_httpd__dependent_vhosts
            }}'


Ansible Facts / Magic Vars
~~~~~~~~~~~~~~~~~~~~~~~~~~

* Always use ``ansible_facts``. Currently, Ansible recognizes both the new fact naming system (using ``ansible_facts``) and the old pre-2.5 "facts injected as separate variables" naming system. The old naming system will be deprecated in a future release of Ansible.


Documenting Variables
~~~~~~~~~~~~~~~~~~~~~

* Document variables in the ``README``. Have a look at ``httpd-apache/README.md`` on how this could look like.


Handling default values
~~~~~~~~~~~~~~~~~~~~~~~

1. A Jinja template contains vendor defaults using ``{{ variable|d('vendor-default-value') }}``.
2. Is overridden by ``defaults/main.yml`` using Linuxfabrik's best practice value ``variable: linuxfabrik-default-value``.
3. May be overriden by the customer by using a ``group_vars`` or ``host_vars``  definition.


Credits
-------

* https://github.com/whitecloud/ansible-styleguide
* https://redhat-cop.github.io/automation-good-practices
* https://docs.openstack.org/openstack-ansible/latest/contributor/code-rules.html
