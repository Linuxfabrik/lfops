# Ansible Role linuxfabrik.lfops.files

This role manages file system entities such as files, directories and symlinks.


## Optional Requirements

* It is recommeded to set `inventory_ignore_patterns = '(host|group)_files'` in your `ansible.cfg` on the Ansible Controller to ignore files in `inventory_dir/host_files`.


## Tags

| Tag     | What it does                             |
| ---     | ------------                             |
| `files` | Manages files, directories and symlinks. |


## Optional Role Variables

| Variable | Description | Default Value |
| -------- | ----------- | ------------- |
| `files__directories__host_var` / <br> `files__directories__group_var` | List of dictionaries containing the directories to manage. Subkeys:<ul><li>`path`: Mandatory, string. Path to the directory.</li><li>`state`: Optional, string. State of the directory, one of `present`, `absent`. Defaults to `present`. Note: both operations are recursive.</li><li>`mode`: Optional, string. Mode (permissions) of the directory. Defaults to `0o755`.</li><li>`owner`: Optional, string. Owner of the directory. Defaults to `root`.</li><li>`group`: Optional, string. Group of the directory. Defaults to `root`.</li></ul> | `[]` |
| `files__files__host_var` / <br> `files__files__group_var` | List of dictionaries containing the files to manage. Subkeys:<ul><li>`path`: Mandatory, string. Path to the file.</li><li>`content`: Optional, string. Content of the file. If unset, the role copies the file from `inventory_dir ~ "/host_files/" ~ inventory_hostname ~ "/" ~ item["path"]`.</li><li>`state`: Optional, string. State of the file, one of `present`, `absent`. Defaults to `present`.</li><li>`mode`: Optional, string. Mode (permissions) of the file. Defaults to `0o644`.</li><li>`owner`: Optional, string. Owner of the file. Defaults to `root`.</li><li>`group`: Optional, string. Group of the file. Defaults to `root`.</li><li>`template`: Optional, boolean. Whether to process file as Jinja template. Note: only works if `content` is unset. Defaults to `false`.</li></ul> | `[]` |
| `files__symlinks__host_var` / <br> `files__symlinks__group_var` | List of dictionaries the symlinks to manage. Subkeys:<ul><li>`src`: Mandatory, string. Path to source of the symlink.</li><li>`dest`: Mandatory, string. Path to dest of the symlink.</li><li>`state`: Optional, string. State of the symlink, one of `present`, `absent`. Defaults to `present`.</li><li>`mode`: Optional, string. Mode (permissions) of the directory. Defaults to `0o644`.</li><li>`owner`: Optional, string. Owner of the directory. Defaults to `root`.</li><li>`group`: Optional, string. Group of the directory. Defaults to `root`.</li></ul> | `[]` |

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
