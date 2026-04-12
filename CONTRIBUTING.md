# Contributing


## Linuxfabrik Standards

The following standards apply to all Linuxfabrik repositories.


### Code of Conduct

Please read and follow our [Code of Conduct](CODE_OF_CONDUCT.md).


### Issue Tracking

Open issues are tracked on GitHub Issues in the respective repository.


### Pre-commit

Some repositories use [pre-commit](https://pre-commit.com/) for automated linting and formatting checks. If the repository contains a `.pre-commit-config.yaml`, install [pre-commit](https://pre-commit.com/#install) and configure the hooks after cloning:

```bash
pre-commit install
```


### Commit Messages

Commit messages follow the [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) specification:

```
<type>(<scope>): <subject>
```

If there is a related issue, append `(fix #N)`:

```
<type>(<scope>): <subject> (fix #N)
```

`<type>` must be one of:

- `chore`: Changes to the build process or auxiliary tools and libraries
- `docs`: Documentation only changes
- `feat`: A new feature
- `fix`: A bug fix
- `perf`: A code change that improves performance
- `refactor`: A code change that neither fixes a bug nor adds a feature
- `style`: Changes that do not affect the meaning of the code (whitespace, formatting, etc.)
- `test`: Adding missing tests


### Changelog

Document all changes in `CHANGELOG.md` following [Keep a Changelog](https://keepachangelog.com/en/1.1.0/). Sort entries within sections alphabetically.


### Language

Code, comments, commit messages, and documentation must be written in English.


### Coding Conventions

- Sort variables, parameters, lists, and similar items alphabetically where possible.
- Always use long parameters when using shell commands.
- Use RFC [5737](https://datatracker.ietf.org/doc/html/rfc5737), [3849](https://datatracker.ietf.org/doc/html/rfc3849), [7042](https://datatracker.ietf.org/doc/html/rfc7042#section-2.1.1), and [2606](https://datatracker.ietf.org/doc/html/rfc2606) in examples and documentation:
    - IPv4: `192.0.2.0/24`, `198.51.100.0/24`, `203.0.113.0/24`
    - IPv6: `2001:DB8::/32`
    - MAC: `00-00-5E-00-53-00` through `00-00-5E-00-53-FF` (unicast), `01-00-5E-90-10-00` through `01-00-5E-90-10-FF` (multicast)
    - Domains: `*.example`, `example.com`


---


## Ansible Development Guidelines

To see these concepts in practice, have a look at the [example role](https://github.com/Linuxfabrik/lfops/tree/main/roles/example).


### Style Guide

YAML:

* Do not use `---` at the top of YAML files. It is only required if one specifies YAML directives above it.
* For YAML files, use the `.yml` extension. This is consistent with `ansible-galaxy init`.
* In YAML files, use 2 spaces for indentation. Elsewhere prefer 4 spaces.
* Use `true` / `false` instead of `yes` / `no`, as they are actually part of YAML.
* Always quote strings and prefer single quotes over double quotes. The only time you should use double quotes is when they are nested within single quotes (e.g. Jinja map reference), or when the string requires escaping characters (e.g. using `\n` to represent a newline). Even though strings are the default type for YAML, syntax highlighting looks better when types are set explicitly. It also helps troubleshooting malformed strings.
* If you must write a long string, use the "folded scalar" (`>` converts newlines to spaces, `|` keeps newlines) style and omit all special quoting.
* Do not quote booleans (e.g. `true`/`false`).
* Do not quote numbers (e.g. `42`).
* Do not quote octal numbers (e.g. `0o755`).
* Insert whitespaces around Jinja filters like so: `{{ my_var | d("my_default") }}`.
* Indent list items:

    Do:

    ```yaml
    list1:
      - item1
      - item2
    ```

    Don't:

    ```yaml
    list2:
    - item1
    - item2
    list3: [ 'tag1', 'tag2' ]
    ```

Ansible:

* Keep 2 empty lines before each `- block:`.
* Prefer `item["subkey"]` to `item.subkey`, since that notation always works.
* Do not use special characters other than underscores in variable names.
* Try to name tasks after their respective shell commands. This makes it easy for sysadmins to understand what is going on.
* Do not use colons at the end of task names. `- name: 'Combined Users:'` renders as `Combined Users:]` in the output.
* Split long Jinja2 expressions into multiple lines.
* Always use `| length > 0` instead of bare `| length` in conditionals. Ansible 2.19+ requires conditional results to be bool, not int.
* Use the `| bool` filter when using bare variables (expressions consisting of just one variable reference without any operator). This guards against YAML quoting mistakes where a boolean ends up as a string: in a `when:` clause, the string `'false'` is truthy (non-empty string) and would incorrectly evaluate to true without `| bool`. Applying it consistently — including in module parameters where Ansible's type coercion would handle it — avoids having to think about where it matters.
* Order module parameters semantically, not alphabetically. The general order is: first identify the target, then describe the action, then set ownership and permissions. For example:

    ```yaml
    - name: 'mkdir -p /etc/example'
      ansible.builtin.file:
        path: '/etc/example'
        state: 'directory'
        owner: 'root'
        group: 'root'
        mode: 0o755

    - name: 'Deploy /etc/example/example.conf'
      ansible.builtin.template:
        backup: true
        src: 'etc/example/example.conf.j2'
        dest: '/etc/example/example.conf'
        owner: 'root'
        group: 'root'
        mode: 0o644
    ```

    This is an exception to the general "sort alphabetically" rule, as alphabetical ordering would obscure what the task operates on.

Commit scopes:

* Use the role or playbook path as commit scope:

    ```
    fix(roles/graylog_server): prevent warn on receiveBufferSize (fix #341)
    ```

* For the first commit, use the message `Add roles/<role-name>` or `Add playbooks/<playbook-name>`.


### Deliverables

When creating a new role, make sure to deliver:

* The role itself.
* `roles/<role-name>/README.md`, following `roles/example/README.md` as a template.
* `roles/<role-name>/meta/argument_specs.yml` declaring all user-facing variables.
* Update `playbooks/README.md`.
* Update `playbooks/all.yml`.
* Update `COMPATIBILITY.md`.
* Update `CHANGELOG.md`.


### Playbooks

* Each playbook must contain all dependencies to run flawlessly against a newly installed machine.
* Playbooks installing an application together with software packages that are complex to configure (`apache_httpd`, `mariadb_server` and/or `php`) as a dependency are prefixed by `setup_`. Example: `setup_nextcloud` because Nextcloud also needs Apache httpd, MariaDB Server etc.
* The name of the playbook should be `- name: 'Playbook linuxfabrik.lfops.example'`.
* After creating a new playbook, document it in `playbooks/README.md` and add it in the `playbooks/all.yml`.
* Every run of the playbooks should be logged to `/var/log/linuxfabrik-lfops.log`. Include the following code in the playbook for this:

    ```yaml
    pre_tasks:
      - ansible.builtin.import_role:
          name: 'shared'
          tasks_from: 'log-start.yml'
        tags:
          - 'always'

    roles:

      - role: 'example'

    post_tasks:
      - ansible.builtin.import_role:
          name: 'shared'
          tasks_from: 'log-end.yml'
        tags:
          - 'always'
    ```


### Roles

* To understand/use a role, reading the README must be enough.
* Idempotency: Roles should not perform changes when applied a second time to the same system with the same parameters, and they should not report that changes have been done if they have not been done. More importantly, it should not damage an existing installation when applied a second time (even without tags). Example:
    ```yaml
    - name: 'Create new DBA "{{ mariadb_root["user"] }}" after a fresh installation'
      ansible.builtin.command: 'mysql --unbuffered --execute "{{ item }}"'
      loop:
        - 'create user if not exists "{{ mariadb_root["user"] }}"@"%" identified by "{{ mariadb_root.password }}";'
        - 'grant all privileges on *.* to "{{ mariadb_root["user"] }}"@"%" with grant option;'
        - 'flush privileges;'
      register: 'mariadb_new_dba_result'
      changed_when: 'mariadb_new_dba_result["stderr"] is not match("ERROR \d+ \(28000\).*")'
      failed_when: 'mariadb_new_dba_result["rc"] != 0 and mariadb_new_dba_result["stderr"] is not match("ERROR \d+ \(28000\).*")'
    ```
* If a role was run without tags, it should deliver a completely installed application (assuming it installs an application).
* Do not over-engineer the role during the development — it should fulfill its use case, but can grow and be improved on later.
* There should be one role per software application. If there are multiple versions of the software, e.g. PHP 7.1, 7.2, 7.3, etc., they all should be supported by a single role.
* Do not use role dependencies via `meta/main.yml`. Dependencies are handled in playbooks.
* Whenever the role requires a list as an input, use a list of dictionaries with `state: present/absent`. See "Combined Variables" below.
* Fail loudly. Avoid constructs that could suppress error messages, like `IfModule` in Apache HTTPd. This makes debugging and troubleshooting a lot easier.
* Do not support software versions that are EOL.
* When implementing a role for a new application, consider security, monitoring and backups.
* For mailing, use the `sendmail` utility, as it provides a consistent interface across distros.
* All user-facing information should be included in the README. Comments are intended for developers only.
* Avoid breaking changes as far as possible, but don't let them stand in the way of improvements.
* Document all changes in the [CHANGELOG.md](https://github.com/Linuxfabrik/lfops/blob/main/CHANGELOG.md) file.


#### Tasks

* Always use the FQCN of the module.
* Always use meta modules wherever possible:
    * `ansible.builtin.package` instead of `ansible.builtin.yum`, `ansible.builtin.dnf` or `ansible.builtin.apt`
    * `ansible.builtin.service` instead of `ansible.builtin.systemd`
* Use the following modules in preference to their alternatives:
    * `ansible.builtin.command` or `ansible.windows.win_command` over `ansible.builtin.shell` over `ansible.builtin.raw`
    * `ansible.builtin.template` over `ansible.builtin.copy`, `ansible.builtin.lineinfile` or `ansible.builtin.blockinfile`. Templating the whole file leads to more consistent, deterministic, and expected results.
* Do not use `state: 'latest'` for the `ansible.builtin.package` module as this is not idempotent. Always use `state: 'present'`.
* Always use `delegate_to: 'localhost'` instead of `local_action`.
* Always provide `changed_when`, `creates`, or `removes` for `ansible.builtin.command` and `ansible.builtin.shell` tasks to ensure idempotency. Use `changed_when: false` for read-only commands.
* When deploying files with `ansible.builtin.template`, always set `backup`, `src`, `dest`, `owner`, `group`, and `mode`.
* Prefer `ansible.builtin.assert` over `ansible.builtin.fail` with `when` for validation checks. There is basically no technical difference; this guideline is only for consistency.
* Optionally add `ansible.builtin.debug` tasks for `__combined_var` variables so the user can see what the role will do.
* Split the service `enabled` and `state` into separate tasks. This is relevant for handlers that would restart the service, see "Handlers" below.
* Always check if SELinux is enabled before managing ports, file contexts, or booleans:

    ```yaml
    - name: 'semanage port --add --type example_port_t --proto tcp 8080'
      community.general.seport:
        ports: 8080
        proto: 'tcp'
        setype: 'example_port_t'
        state: 'present'
      when:
        - 'ansible_facts["selinux"]["status"] != "disabled"'
    ```


#### Handlers

* Use handlers in favor to `some_result is changed` if no `meta: flush_handlers` is required or if it would prevent duplicate code.
* Since handlers are global, prefix them with the role name to make sure the correct one is used.
* Use chained handlers (notify) when a validation step should precede the actual action, e.g. a config validation handler that notifies a restart handler.
* Handlers that restart or reload a service should skip execution when the service was just started (redundant) or when the user wants it stopped. For this, the result of the service state task has to be registered and checked. Example:

    ```yaml
    - name: 'example: restart example'
      ansible.builtin.service:
        name: 'example'
        state: 'restarted'
      when:
        - '__example__service_state_result is not changed'
        - 'example__service_state != "stopped"'
    ```


#### Tags

* Naming scheme: `role_name` and `role_name:section`. For example `apache_httpd` and `apache_httpd:vhosts`.
* The role should only do what one expects from the tag name. For example, the `mariadb:user` tag only manages MariaDB users.
* The README of a role should provide a list of the available tags and what they do.
* The tags should be set in the role itself. Do not set them in the playbook.
* Blocks/tasks that install base packages do not require tags such as `apache:pkgs`, `apache:setup` or `apache:install`. There is no real world scenario where it makes sense to only run the installation via Ansible, some configuration is always required.
* For each task, consider to which areas it belongs. A task will usually have multiple tags.


#### Variables

* `./vars`: Variables that are not to be edited by users.
* `./defaults`: Default variables for the role, might be overridden by the user in the inventory.
* Document all user-facing variables in the README. Have a look at `roles/example/README.md` for the format.
* Do not set defaults for mandatory variables.
* Naming scheme: `<role name>__<optional: config file>_<setting name>`, for example `apache_httpd__server_admin`.
* No need to invent new names, use the key-names from the config file (if possible), for example `redis__conf_maxmemory`.
* Prefix role-internal variables with `__`, for example `__example__sysconfig_path`. This makes it easy to determine which variables are user-facing and therefore should be in the README.
* Avoid embedding large lists or "magic values" directly into the playbook. Such static lists should be placed into the `vars/main.yml` file and named appropriately.
* If you need random but predictable/idempotent values, use the `inventory_hostname` as seed. Example for setting the minutes of an hour: `{{ 59 | random(seed=inventory_hostname) }}`.
* When guarding optional role variables (strings or lists) that may be undefined, use `is defined and my_var | length > 0`. This catches both undefined variables and empty values (e.g. `my_var: ''`). Bare `is defined` is fine for dict subkeys where presence alone is the signal (e.g. `item["cidr"] is defined`) or for result attributes (e.g. `result["failed"] is defined`).
* Any secrets (passwords, tokens etc.) should not be provided with default values in the role. It is important for a secure-by-default implementation to ensure that an environment is not vulnerable due to the production use of default secrets. Users must be forced to properly provide their own secret variable values.
* Always use the `ansible_facts` dictionary (e.g. `ansible_facts["os_family"]` instead of `ansible_os_family`). The old pre-2.5 "facts injected as separate variables" naming system will be deprecated in a future release of Ansible.


##### Variable Validation with `argument_specs`

Every role should include a `meta/argument_specs.yml` that declares all user-facing variables with their types. Ansible validates these automatically at role entry (before any tasks run), catching type mismatches and missing required variables without manual assert code.

Include all variables documented in the README: mandatory variables, simple optional variables, and the `__host_var`/`__group_var` variants of injection variables. Do not include internal variables (`__dependent_var`, `__role_var`, `__combined_var`).

Guidelines for `argument_specs`:

* Use `required: true` for mandatory variables (replaces manual `assert` + `is defined` checks).
* Use `type` and `choices` where applicable. For injection variables where the default is `''` (empty string) but the actual value is a different type (e.g. int), use `type: 'raw'` to avoid rejecting the empty default.
* Omit `default` when the default in `defaults/main.yml` is a Jinja2 expression (e.g. `'{{ __example__conf_worker_threads }}'`), as `argument_specs` cannot evaluate it.
* Set `default` when it is a static value (e.g. `true`, `'started'`, `[]`).
* Sort entries alphabetically.

Use `ansible.builtin.assert` in the tasks for validations that `argument_specs` cannot express: value ranges, regex patterns, or cross-variable dependencies. Tag the assert block with `always` so it runs even when other roles reference the validated variables.

Have a look at the `example` role's `meta/argument_specs.yml` for a complete reference.


##### Combined Variables

The goal of combined variables is that variables can be set in multiple places, and then merged in order to be used in the role. For example, the user can overwrite a specific configuration role default (`__role_var`) from their inventory (`__host_var` / `__group_var`).

Furthermore, other roles can also inject their sensible defaults via the `__dependent_var`, with a higher precedence than the role defaults, but lower than the user's inventory.

To enable this behavior, you must define the `__combined_var` as follows:
```yaml
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
```

The `__combined_var` will then be used in the tasks or templates of the role.

The role must always implement some sort of `state` key, otherwise the user cannot unset a value defined in the defaults. Suppose the user wants to disable the default localhost vHost of the Apache HTTPd role:
```yaml
# defaults/main.yml
apache_httpd__vhosts__role_var:
  - conf_server_name: 'localhost'
    virtualhost_port: 80
    template: 'localhost'
```

Without the `state` key, the user has no way of achieving this, as they cannot remove previously defined elements from the list via the inventory. With the `state` key, the role knows it has to remove the vHost:
```yaml
# inventory
apache_httpd__vhosts__role_var:
  - conf_server_name: 'localhost'
    virtualhost_port: 80
    state: 'absent'
```

The handling of the state in the role should look something like this, assuming the default value for `state` is `present`:
```yaml
- name: 'Remove sites-available vHosts'
  ansible.builtin.file:
    path: '...'
    state: 'absent'
  loop: '{{ apache_httpd__vhosts__combined_var }}'
  loop_control:
    label: '{{ item["name"] }}'
  when:
    - 'item["state"] | d("present") == "absent"'

- name: 'Create sites-available vHosts'
  ansible.builtin.template:
    src: '...'
    dest: '...'
  loop: '{{ apache_httpd__vhosts__combined_var }}'
  loop_control:
    label: '{{ item["name"] }}'
  when:
    - 'item["state"] | d("present") != "absent"'
```

Other times it is useful to generate a list of present and absent elements, for example when using `ansible.builtin.package`, as providing the packages as a list is much faster than looping through them.
```yaml
- name: 'Ensure PHP modules are absent'
  ansible.builtin.package:
    name: '{{ php__modules__combined_var | selectattr("state", "defined") | selectattr("state", "eq", "absent") | map(attribute="name") }}'
    state: 'absent'

- name: 'Ensure PHP modules are present'
  ansible.builtin.package:
    name: '{{ (php__modules__combined_var | selectattr("state", "defined") | selectattr("state", "ne", "absent") | map(attribute="name"))
        + (php__modules__combined_var | selectattr("state", "undefined") | map(attribute="name")) }}'
    state: 'present'
```

Or in a Jinja2 template:
```
{% for item in apache_tomcat__roles__combined_var if item['state'] | d('present') != 'absent' %}
<role rolename="{{ item['name'] }}"/>
{% endfor %}
```

The vHost example above can be used to demonstrate another feature of `linuxfabrik.lfops.combine_lod`. Normally, the list items are combined based on a `unique_key` that should match, for example, the `name` key. However, this does not work with `conf_server_name` because you can have a vHost with the same `conf_server_name` for multiple ports. This means that the `unique_key` must be a *combination* of `conf_server_name` and `virtualhost_port`:
```yaml
apache_httpd__vhosts__combined_var: '{{ (
      apache_httpd__vhosts__role_var +
      apache_httpd__vhosts__dependent_var +
      apache_httpd__vhosts__group_var +
      apache_httpd__vhosts__host_var
    ) | linuxfabrik.lfops.combine_lod(unique_key=["conf_server_name", "virtualhost_port"])
  }}'
```

Note:

* Have a look at `ansible-doc --type filter linuxfabrik.lfops.combine_lod`.
* Always use lists of dictionaries or simple values. Never use dictionaries directly, even though they allow overwriting of earlier elements, since one cannot template the keyname using Jinja2. This would prevent passing on of variables, especially in `__dependent_var` (for details have a look at <https://docs.linuxfabrik.ch/software/ansible.html#besonderheiten-von-ansible>).
* Simple value `__combined_var` are always returned as strings. Convert them to integers when needed.


##### `skip_role` Variables in Playbooks

The `playbook_name__role_name__skip_role` and `playbook_name__role_name__skip_role_injections` variables should provide the user an option to skip the role and the role's injections respectively. Have a look at the [README.md](./README.md#skipping-roles-in-a-playbook).

For this, we need to set the following two internal variables at the top of the playbook (between the `hosts:` and `roles:`):

```yaml
vars:

  setup_icinga2_master__icingaweb2__skip_injections__internal_var: '{{ setup_icinga2_master__icingaweb2__skip_injections | d(setup_icinga2_master__icingaweb2__skip_role__internal_var) }}'
  setup_icinga2_master__icingaweb2__skip_role__internal_var:       '{{ setup_icinga2_master__icingaweb2__skip_role       | d(false) }}'
```

Then use them with the roles as follows:

```yaml
- role: 'linuxfabrik.lfops.icingaweb2'
  when:
    - 'not setup_icinga2_master__icingaweb2__skip_role__internal_var'

- role: 'linuxfabrik.lfops.mariadb_server'
  mariadb_server__databases__dependent_var: '{{
      (not setup_icinga2_master__icingaweb2__skip_injections__internal_var) | ternary(icingaweb2__mariadb_server__databases__dependent_var, [])
    }}'
  mariadb_server__users__dependent_var: '{{
      (not setup_icinga2_master__icingaweb2__skip_injections__internal_var) | ternary(icingaweb2__mariadb_server__users__dependent_var, []) +
    }}'
```

Make sure to use the following format when passing multiple injections to avoid needing to flatten the list:

```yaml
- role: 'linuxfabrik.lfops.icinga2_master'
  icinga2_master__api_users__dependent_var: '{{
      (not setup_icinga2_master__icingadb__skip_injections__internal_var) | ternary(icingadb__icinga2_master__api_users__dependent_var, []) +
      (not setup_icinga2_master__icingaweb2_module_director__skip_injections__internal_var) | ternary(icingaweb2_module_director__icinga2_master__api_users__dependent_var, []) +
      (not setup_icinga2_master__icingaweb2__skip_injections__internal_var) | ternary(icingaweb2__icinga2_master__api_users__dependent_var, [])
    }}'
```


#### Templates

* Always use the `ansible.builtin.template` module instead of the `ansible.builtin.copy` module, even if there are currently no variables in the file. This makes it easier to extend later on, and allows the usage of an automatically generated header.
* Always create a backup file including the timestamp information (e.g. `keycloak.conf.23875.2025-02-14@15:19:16~`) so you can get the original file back if you somehow clobbered it incorrectly, by using `backup: true`.
* Always add the following to the top of templates, using the appropriate comment syntax:
    ```
    # {{ ansible_managed }}
    # 2021081601
    ```
* Do not use `{{ template_run_date }}` inside the template. It is the date that the template was rendered, which is done during every Ansible run. This means that the task will always be changed, even if nothing else changed in the template, therefore breaking idempotency.
* Use the target path for the file in the `template` folder, for example: `templates/etc/httpd/sites-available/default.conf.j2`. This makes it clear what the file is for, and avoids name collisions.
* Always use the `.j2` file extension for files in the `template` folder.
* If deploying self-written scripts, copy them to `/usr/local/sbin` (due to SELinux).
* Keep templates as close to the original file as possible. This makes handling of rpmnew/rpmsave files easier.
* Add the following task after deploying a file that might get rpmnew or rpmsave files (or their Debian equivalents):
    ```yaml
    - name: 'Remove rpmnew / rpmsave (and Debian equivalents)'
      ansible.builtin.include_role:
        name: 'shared'
        tasks_from: 'remove-rpmnew-rpmsave.yml'
      vars:
        shared__remove_rpmnew_rpmsave_config_file: '{{ item }}'
      loop: '{{ repo_epel__repo_files }}'
    ```


#### OS-specific Variables

If some variables need to be parameterized according to distribution and version (name of packages, configuration file paths, names of services), use OS-specific vars-files inside the `vars/` of your role.

Variables with the same name are overridden by the files in `vars/` in order from least specific to most specific:

* `os_family` covers a group of closely related platforms (e.g. `RedHat` covers `RHEL`, `CentOS`, `Fedora`)
* `distribution` (e.g. `CentOS`) is more specific than os_family
* `distribution_major_version` (e.g. `CentOS7`) is more specific than distribution
* `distribution_version` (e.g. `CentOS7.9`) is the most specific

To load the variables include the `platform-variables.yml` in the `tasks/main.yml` like this:
```yaml
- name: 'Set platform/version specific variables'
  ansible.builtin.import_role:
    name: 'shared'
    tasks_from: 'platform-variables.yml'
  tags:
    - 'always'
```

Use the `always` tag so the variables are available even when running with a specific tag — other roles in the playbook may reference these variables.

Note that since `vars/` are higher up in the [Ansible variable precedence](https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_variables.html#understanding-variable-precedence) than inventory variables we cannot directly define our defaults there. Instead, we either need to use the `my_role__my_var__role_var` (as these already support overwriting of `role_vars`; see "Combined Variables") or to define an internal variable (prefixed with `__`) in the `vars/` file:

```yaml
__my_role__my_simple_value: 'os-dependant default'
```

Then, in `defaults/main.yml`, we reference that internal variable as our public default:

```yaml
my_role__my_simple_value: '{{ __my_role__my_simple_value }}'
```

This allows the user to overwrite `my_role__my_simple_value` in their inventory.


#### OS-specific Tasks

In order to run only certain tasks based on the operating system platform, files need to be placed in `tasks/` with the filename of the supported "os family".

Assume you have the following OS-specific task files, in order of most specific to least specific:

* `tasks/CentOS7.4.yml`
* `tasks/CentOS7.yml`
* `tasks/RedHat.yml`
* `tasks/main.yml`

Now, if you run Ansible against a *CentOS 7.9* host, for example, only these tasks are processed in the following order:

1. `tasks/CentOS7.yml`
2. `tasks/main.yml`

Include the OS-specific tasks in the `tasks/main.yml` like this:

```yaml
- name: 'Perform platform/version specific tasks'
  ansible.builtin.include_tasks: '{{ __task_file }}'
  when: '__task_file | length > 0'
  vars:
    __task_file: '{{ lookup("ansible.builtin.first_found", __first_found_options) }}'
    __first_found_options:
      files:
        - '{{ ansible_facts["distribution"] }}{{ ansible_facts["distribution_version"] }}.yml'
        - '{{ ansible_facts["distribution"] }}{{ ansible_facts["distribution_major_version"] }}.yml'
        - '{{ ansible_facts["distribution"] }}.yml'
        - '{{ ansible_facts["os_family"] }}{{ ansible_facts["distribution_version"] }}.yml'
        - '{{ ansible_facts["os_family"] }}{{ ansible_facts["distribution_major_version"] }}.yml'
        - '{{ ansible_facts["os_family"] }}.yml'
      paths:
        - '{{ role_path }}/tasks'
      skip: true
  tags:
    - 'always'
```

Make sure to set the tags directly on the `include_tasks` task, and not on a surrounding block. Setting it on a block causes the tag to be inherited to all tasks in that block, therefore also to included tasks.


### Handling of GPG Keys under Debian (APT Keyring)

Adding a key to `/etc/apt/trusted.gpg.d` is insecure because it adds the key for all repositories. Therefore, `apt-key` (and the `ansible.builtin.apt_key` module) were deprecated.

The new and secure workflow is:

1. Store the GPG key in `/etc/apt/keyrings/`. The file extension **has** to match the file format. Use the `file` utility to determine the format:
    * `PGP public key block Public-Key (old)`: ASCII-armored key. Use `.asc` extension.
    * `OpenPGP Public Key`: Binary GPG key. Use `.gpg` extension.

2. Explicitly specify the path to the key in the `/etc/apt/sources.list.d/` file, for example: `deb [signed-by=/etc/apt/keyrings/icinga.asc] https://...`.

Have a look at the [repo_icinga/tasks/Debian.yml](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_icinga/tasks/Debian.yml) (ASCII armored key) or [repo_mariadb/tasks/Debian.yml](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_mariadb/tasks/Debian.yml) (binary GPG key) roles.


### Roles with Special Features

Roles with special technical implementations and capabilities:

* [apache_solr](https://github.com/Linuxfabrik/lfops/tree/main/roles/apache_solr): Installs the correct version of a dependent package (i.e. java) based on the solr version.

* [github_project_createrepo](https://github.com/Linuxfabrik/lfops/tree/main/roles/github_project_createrepo): Sets FACL entries to allow both the webserver user and the github-project-createrepo user to access files.

* [librenms](https://github.com/Linuxfabrik/lfops/tree/main/roles/librenms): Compiles and loads an SELinux module.

* [mongodb](https://github.com/Linuxfabrik/lfops/tree/main/roles/mongodb): The role implements a `skip` state that completely ignores the entry.

* [monitoring_plugins](https://github.com/Linuxfabrik/lfops/tree/main/roles/monitoring_plugins): Implements install & maintenance as well as uninstall/remove on Linux and Windows.

* [moodle](https://github.com/Linuxfabrik/lfops/tree/main/roles/moodle): Searches for the latest and most recent specific LTS version of itself on GitHub.

* [nextcloud](https://github.com/Linuxfabrik/lfops/tree/main/roles/nextcloud): The role performs some tasks only on the very first run and never again after that. To do this, it creates a state file for itself so that it knows that it must skip certain tasks on subsequent runs. The role's README has a concise but informative "Tags" section.

* [php](https://github.com/Linuxfabrik/lfops/tree/main/roles/php): Build list for ansible.builtin.packages based on state `present` and `absent`. Some Jinja templates use non-default strings marking the beginning/end of a block.

* [redis](https://github.com/Linuxfabrik/lfops/tree/main/roles/redis): Gathers the installed version and deploys the corresponding config file. Configures Systemd with Unit File overrides.

* [telegraf](https://github.com/Linuxfabrik/lfops/tree/main/roles/telegraf): Jinja templates use non-default strings marking the beginning/end of a print statement.

* [wordpress](https://github.com/Linuxfabrik/lfops/tree/main/roles/wordpress): chmod: Sets file and folder permissions separately using `find`.


### Credits

* <https://github.com/whitecloud/ansible-styleguide>
* <https://redhat-cop.github.io/automation-good-practices>
* <https://docs.openstack.org/openstack-ansible/latest/contributor/code-rules.html>
