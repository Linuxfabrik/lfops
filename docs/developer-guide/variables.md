# Variables

* `./vars`: not to be edited by users. `./defaults`: may be overridden in the inventory.
* Document all user-facing variables in the README, formatted as in `roles/example/README.md`.
* No defaults for mandatory variables, and none for secrets (passwords, tokens etc.).
* Software versions are always mandatory, never role defaults: a bumped default silently changes what an existing inventory deploys.
* Add variables where needed, but treat renaming a documented variable, changing its default, or making a previously ignored one take effect as a breaking change, even though nothing fails: Ansible ignores unknown inventory variables without a warning, so an inventory still using the old name silently gets the default.
* Naming: `<role name>__<optional: config file>_<setting name>`, e.g. `apache_httpd__server_admin`, reusing config file key names where possible (`redis__conf_maxmemory`).
* Prefix role-internal variables with `__`, e.g. `__example__sysconfig_path`.
* Put large static lists and "magic values" into `vars/main.yml`, not into the playbook.
* Seed random but idempotent values with `inventory_hostname`: `{{ 59 | random(seed=inventory_hostname) }}`.
* Guard optional strings or lists with `is defined and my_var | length > 0`. Bare `is defined` is fine for dict subkeys where presence is the signal and for result attributes.
* Group credentials as subkeys of one dict (e.g. `<role>__login` with `username`, `password`), matching the `linuxfabrik.lfops.bitwarden_item` lookup.
* Use `ansible_facts["os_family"]`, not `ansible_os_family`.


## Deviating from an Upstream Default

Where a role default differs from what the software ships (as installed from the repository the role uses, which may differ from upstream docs), say so and why. Otherwise the next person either keeps a wrong value or "corrects" a deliberate one.

* Where the value is defined (`defaults/main.yml`, `vars/<version>.yml`, `vars/<os>.yml`), add the value only: `example__conf_max_connections__role_var: 100  # upstream default: 151`.
* A default in `defaults/main.yml` that takes its value from `vars/<os>.yml` keeps the comment on its own line and lists the upstream value per platform: `# upstream default: /run/valkey/valkey.sock on RHEL, off on Debian / Ubuntu` (see `roles/valkey/defaults/main.yml`).
* In the README, add a last bullet below `Default:` with the reasoning in one sentence, for the administrator. Mention version- or platform-specific defaults there ("MariaDB 11.8 ships it on, older releases ship it off"). The reasoning lives in the README only.

    ```markdown
    * Default: `100`
    * Deviates from the upstream default `151`: each connection reserves its own buffers, and 151 of them exhaust the memory of the 2 GB VMs this role is typically deployed on.
    ```

Keep evidence of upstream defaults in the repository where a role needs it, as `roles/mariadb_server/vars/vendor/` does: a `mariadbd --help --verbose` dump per supported version from a clean installation, package recorded in the header, so `git diff` shows moved defaults.


## Variable Validation with `argument_specs`

Every role has a `meta/argument_specs.yml` declaring all variables documented in the README, including the `__host_var` / `__group_var` / `__dependent_var` variants, but not `__role_var` and `__combined_var`. `__dependent_var` is required because `setup_*` playbooks pass it via `vars:`; without it, role entry fails with `Supported parameters include: ...`.

* `required: true` for mandatory variables.
* Use `type` and `choices`. For injection variables with an `''` default but another actual type, use `type: 'raw'`.
* Dicts fed by external lookups (e.g. `bitwarden_item`) get `type: 'dict'` without `options:`, since they carry extra keys; document the expected keys in the README.
* Omit `default` when it is a Jinja2 expression, set it when static (`true`, `'started'`, `[]`).
* Sort entries alphabetically.

What `argument_specs` cannot express (ranges, regexes, cross-variable dependencies) goes into `ansible.builtin.assert` in a block tagged `always`. Reference: `roles/example/meta/argument_specs.yml`.


## Combined Variables

The user overrides *parts* of the role default (`__role_var`) from the inventory (`__host_var` / `__group_var`), and other roles inject defaults via `__dependent_var` (above the role default, below the inventory). Define in `defaults/main.yml`, slots sorted alphabetically; precedence lives in the lazily evaluated expression only:

```yaml
# for list of dictionaries
my_role__my_var__combined_var: '{{ (
      my_role__my_var__role_var +
      my_role__my_var__dependent_var +
      my_role__my_var__group_var +
      my_role__my_var__host_var
    ) | linuxfabrik.lfops.combine_lod
  }}'
my_role__my_var__dependent_var: []
my_role__my_var__group_var: []
my_role__my_var__host_var: []
my_role__my_var__role_var: []

# for simple values like strings, numbers or booleans
my_role__my_var__combined_var: '{{
    my_role__my_var__host_var if (my_role__my_var__host_var | string | length) else
    my_role__my_var__group_var if (my_role__my_var__group_var | string | length) else
    my_role__my_var__dependent_var if (my_role__my_var__dependent_var | string | length) else
    my_role__my_var__role_var
  }}'
my_role__my_var__dependent_var: ''
my_role__my_var__group_var: ''
my_role__my_var__host_var: ''
my_role__my_var__role_var: ''
```

* Always implement a `state` key (default `present`), otherwise the user cannot remove a default element: e.g. the default localhost vHost of `apache_httpd` is removed by setting the same element with `state: 'absent'`. Handle it with `when: 'item["state"] | d("present") == "absent"'` (remove) and `!= "absent"` (create); in templates `{% for item in ... if item['state'] | d('present') != 'absent' %}`. For `ansible.builtin.package`, pass present and absent names as two lists instead of looping (see `roles/php`).
* `combine_lod` merges items on `unique_key` (default `name`); combine several keys where one is not unique, e.g. `combine_lod(unique_key=["conf_server_name", "virtualhost_port"])`. See `ansible-doc --type filter linuxfabrik.lfops.combine_lod`.
* Use lists of dictionaries or simple values, never dictionaries: their key names cannot be templated, which breaks passing values on, especially via `__dependent_var`.
* A simple-value `__combined_var` is always a string; convert it to an integer when needed.


## `skip_role` Variables in Playbooks

`<playbook>__<role>__skip_role` and `<playbook>__<role>__skip_role_injections` let the user skip a role or its injections, see the [README.md](../../README.md#skipping-roles-in-a-playbook). Set two internal variables between `hosts:` and `roles:` and use them:

```yaml
vars:

  setup_icinga2_master__icingaweb2__skip_injections__internal_var: '{{ setup_icinga2_master__icingaweb2__skip_injections | d(setup_icinga2_master__icingaweb2__skip_role__internal_var) }}'
  setup_icinga2_master__icingaweb2__skip_role__internal_var:       '{{ setup_icinga2_master__icingaweb2__skip_role       | d(false) }}'

roles:

  - role: 'linuxfabrik.lfops.icingaweb2'
    when:
      - 'not setup_icinga2_master__icingaweb2__skip_role__internal_var'

  - role: 'linuxfabrik.lfops.icinga2_master'
    # several injections: concatenate, so the list needs no flattening
    icinga2_master__api_users__dependent_var: '{{
        (not setup_icinga2_master__icingadb__skip_injections__internal_var) | ternary(icingadb__icinga2_master__api_users__dependent_var, []) +
        (not setup_icinga2_master__icingaweb2__skip_injections__internal_var) | ternary(icingaweb2__icinga2_master__api_users__dependent_var, [])
      }}'
```


## OS-specific Variables

Put values differing by platform (packages, paths, services) into `vars/` files, overriding from least to most specific: `os_family` (`RedHat`), `distribution` (`CentOS`), `distribution_major_version` (`CentOS7`), `distribution_version` (`CentOS7.9`).

* With a `vars/Debian.yml`, always create an explicit `vars/Ubuntu.yml`, even as an identical copy, so Ubuntu stays visible and drift has a home.
* Load them in `tasks/main.yml` by importing `shared` with `tasks_from: 'platform-variables.yml'`, tagged `always` (other roles may reference them).
* `vars/` outrank the inventory, so user-overridable defaults go into `__role_var` (see "Combined Variables") or into an internal `__my_role__my_value` in `vars/<os>.yml`, referenced from `defaults/main.yml` as `my_role__my_value: '{{ __my_role__my_value }}'`.


## OS-specific Dependent Variables

When a role running *earlier* consumes the value (the `__dependent_var` pattern), `vars/<os>.yml` loads too late. Keep the platform-keyed dictionary internal in the publishing role's `vars/main.yml` (loaded at play parse, visible to every role) and publish a selection via `linuxfabrik.lfops.platform_select`:

```yaml
# roles/mariadb_server/vars/main.yml
__mariadb_server__python__modules__dependent_var:
  Debian:
    - name: 'python3-pymysql'
  RedHat:
    - name: 'python3-PyMySQL'
mariadb_server__python__modules__dependent_var: '{{
    __mariadb_server__python__modules__dependent_var
    | linuxfabrik.lfops.platform_select(ansible_facts, default=[])
  }}'
```

Consumers reference the public variable directly. The filter mirrors `shared/tasks/platform-variables.yml` (least to most specific: `os_family`, `os_family + distribution_major_version`, `os_family + distribution_version`, `distribution`, `distribution + distribution_major_version`, `distribution + distribution_version`); without `default`, an unmatched platform raises an error.

A published `__dependent_var` must be valid on every host, whether or not its role runs there: ansible-core up to 2.18 resolves all variables of an expression, even in an untaken `ternary()` / `if` branch, and `skip_injections: false` uses a skipped role's injection on purpose. So:

* Always pass `default=[]` (or the consumer's empty value) to `platform_select`.
* If the publishing role cannot work without the value, it asserts its supported platforms in its own `always` validation block (reference: `roles/duplicity`).
* Never derive it from a variable the consuming role sets at runtime: a consumer with `argument_specs` templates all parameters at role entry, and one undefined value aborts with `input must be a dict keyed by platform identifier, got AnsibleUndefined`. If unavoidable, publish an empty list until the value exists; the parameter is re-templated on every use:

```yaml
# roles/nextcloud/vars/main.yml
nextcloud__php__modules__dependent_var: '{{
    (__nextcloud__php__modules__dependent_var
      | linuxfabrik.lfops.platform_select(ansible_facts))
    if __php__installed_version is defined else []
  }}'
```


## LFOps-wide Shared Variables

Platform values shared by many roles (currently the Apache httpd user, group and service name) live once in `roles/shared/vars/<os>.yml`, loaded by `roles/shared/tasks/global-variables.yml` in every playbook's `pre_tasks`. Reference them directly (e.g. `group: '{{ __shared__apache_httpd_group }}'`), and add new ones there.
