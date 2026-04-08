# Ansible Role linuxfabrik.lfops.files

This role manages file system entities such as files, directories and symlinks.


## Optional Requirements

* It is recommeded to set `inventory_ignore_patterns = '(host|group)_files'` in your `ansible.cfg` on the Ansible Controller to ignore files in `inventory_dir/host_files`.


## Tags

`files`

* Manages files, directories and symlinks.
* Triggers: none.


## Optional Role Variables

`files__directories__host_var` / `files__directories__group_var`

* List of dictionaries containing the directories to manage.
* Type: List of dictionaries.
* Default: `[]`

* Subkeys:

    * `path`:

        * Mandatory. Path to the directory.
        * Type: String.

    * `state`:

        * Optional. State of the directory, one of `present`, `absent`. Note: both operations are recursive.
        * Type: String.
        * Default: `'present'`

    * `mode`:

        * Optional. Mode (permissions) of the directory.
        * Type: String.
        * Default: `0o755`

    * `owner`:

        * Optional. Owner of the directory.
        * Type: String.
        * Default: `'root'`

    * `group`:

        * Optional. Group of the directory.
        * Type: String.
        * Default: `'root'`

`files__files__host_var` / `files__files__group_var`

* List of dictionaries containing the files to manage.
* Type: List of dictionaries.
* Default: `[]`

* Subkeys:

    * `path`:

        * Mandatory. Path to the file.
        * Type: String.

    * `content`:

        * Optional. Content of the file. If unset, the role copies the file from `inventory_dir ~ "/host_files/" ~ inventory_hostname ~ "/" ~ item["path"]`.
        * Type: String.

    * `state`:

        * Optional. State of the file, one of `present`, `absent`.
        * Type: String.
        * Default: `'present'`

    * `mode`:

        * Optional. Mode (permissions) of the file.
        * Type: String.
        * Default: `0o644`

    * `owner`:

        * Optional. Owner of the file.
        * Type: String.
        * Default: `'root'`

    * `group`:

        * Optional. Group of the file.
        * Type: String.
        * Default: `'root'`

    * `template`:

        * Optional. Whether to process file as Jinja template. Note: only works if `content` is unset.
        * Type: Bool.
        * Default: `false`

`files__symlinks__host_var` / `files__symlinks__group_var`

* List of dictionaries the symlinks to manage.
* Type: List of dictionaries.
* Default: `[]`

* Subkeys:

    * `src`:

        * Mandatory. Path to source of the symlink.
        * Type: String.

    * `dest`:

        * Mandatory. Path to dest of the symlink.
        * Type: String.

    * `state`:

        * Optional. State of the symlink, one of `present`, `absent`.
        * Type: String.
        * Default: `'present'`

    * `mode`:

        * Optional. Mode (permissions) of the directory.
        * Type: String.
        * Default: `0o644`

    * `owner`:

        * Optional. Owner of the directory.
        * Type: String.
        * Default: `'root'`

    * `group`:

        * Optional. Group of the directory.
        * Type: String.
        * Default: `'root'`

Example:
```yaml
# optional
files__directories__host_var:
  - path: '/data/a'
  - path: '/data/b'
    mode: 0o770
  - path: '/data/b/c'
    owner: 'apache'
files__files__host_var:
  - path: '/data/file1'
    # just use `|` so that there is a newline at the end of the file
    content: |
      echo "a script with
      multiple lines"
    mode: 0o755
  - path: '/data/file2' # content will be taken from `inventory_dir/host_files/inventory_hostname/data/file3`
  - path: '/data/file3'
    state: 'absent'
  - path: '/etc/hosts'
    content: '{{ lookup("ansible.builtin.file", inventory_dir ~ "/group_files/all/etc/hosts") }}'
    mode: 0o644
    owner: 'root'
    group: 'root'
files__symlinks__host_var:
  - src: '/data/file1'
    dest: '/data/file1_link'
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
