# Tools

`lfops` is for running LFOps playbooks. The other files in this directory are for the development of LFOps, `follow-upstream` and `maintenance.yml` are described in the [developer guide](../docs/developer-guide/upstream.md).


## lfops

`lfops` is a terminal UI that assembles and starts an `ansible-navigator run` of an LFOps playbook. It walks through five steps, playbook > tags > inventories > limit > confirm, and finds everything on its own:

* Playbooks: the `playbooks/*.yml` of the LFOps checkout (see `LFOPS_DIR` below) that have hosts in at least one inventory.
* Tags: the roles a playbook runs (including imported playbooks, `import_role`, `include_role` and role dependencies), and for each role the tags documented in the "Tags" section of its README.
* Inventories: the ones with hosts in the groups the playbook targets (`hosts:` of its plays). An inventory without such hosts is offered if another playbook runs the role there, with the role as tag. Selecting it switches to that playbook, for example from `monitoring_plugins` to `setup_basic --tags=monitoring_plugins`.
* Limit: the hosts of the selected inventories in the groups the playbook targets, plus the groups these hosts are in. Typed text such as `060-t-*` is offered as a pattern of its own.
* Confirm: the command, the number of hosts it targets and the first 10 of them. The limit is resolved like Ansible does, on the merged group structure of the selected inventories, for host and group names, globs, `&` and `!`. Other patterns (`~regex`, `@file`, `group[0:2]`, `host:port`, IPv6 addresses) show the number as unknown. It is an estimate: `when` conditions other than the skip variables of a role, `group_by` and `add_host` are not evaluated.

Every page shows the command as it stands with the selection of the page, the arguments the page sets in green, and the number of hosts it targets. Inventories below `$LF_GITLAB` are shown relative to it, as `--inventory=$LF_GITLAB/060/ans/hosts.yml`; the command the tool prints and runs has the full path. Arguments are quoted only where bash needs it, for example `'--limit=060-t-*'`.

Playbooks, inventories, tags, limits and options used last are listed first. Ctrl-R lists the complete runs, used last first: choosing one fills in all steps and shows the confirm page, Esc then goes back through the steps with its values selected. Typing filters the list: entries containing the text come first, then the ones containing its letters in order (`setbas` finds `setup_basic`), then the ones with the text in their description.

On the confirm page, `c` and `d` switch `--check` and `--diff` on and off, and `f` lists further options (`--verbose` and the ones used before) and takes typed text as an argument for ansible-navigator, for example `--extra-vars=lfops__reboot_now=true`. Typed text cannot contain spaces. Any argument the tool does not know itself starts switched on; an option and its value become one entry (`-e x=y` becomes `--extra-vars=x=y`, `-C` becomes `--check`):

```bash
lfops --check --diff
lfops --extra-vars='lfops__reboot_now=true'
```

After the confirmation, the tool prints the command and runs it through a login shell (`bash -lc`), so an `ansible-navigator` shell function from `/etc/profile.d/` is used if there is one.


### Installation

The tool needs Python 3.8 or newer with PyYAML (`python3-pyyaml`, `python3-yaml` on Debian) and runs from a clone of the repository. Put it on the `PATH`, for example with a symlink:

```bash
ln --symbolic /path/to/lfops/tools/lfops ~/.local/bin/lfops
```

On RHEL 8, `python3` is Python 3.6. Install `python3.11` and `python3.11-pyyaml` and use a wrapper script instead of the symlink:

```bash
printf '#!/bin/sh\nexec python3.11 /path/to/lfops/tools/lfops "$@"\n' > ~/.local/bin/lfops
chmod +x ~/.local/bin/lfops
```

The tool works under any name: a link `~/.local/bin/lfo` makes it `lfo`, and the shell integration below then defines the function `lfo`. The name starts with a letter or `_`, followed by letters, digits, `_` and `-`.


### Keys

* Type to filter, Backspace to delete a character, Ctrl-U to clear the filter.
* Up, Down, PgUp, PgDn, Home and End to move.
* Space or Tab to (de)select an entry, Ctrl-A to (de)select all visible entries. In the playbook step, which takes a single entry, Space and Tab continue like Enter.
* Enter to continue with the selected entries, or without a selection with the highlighted one. Enter on typed text adds it to the selection.
* Esc to go back a step, the selection of the steps is kept. Choosing another playbook starts the later steps empty, choosing other inventories clears the limit.
* Ctrl-R to choose a past run, Ctrl-C to quit.
* On the confirm page: Enter to run, `c` for `--check`, `d` for `--diff`, `f` for further options.


### Options

* `--print-only`: print the command instead of running it. The UI draws on the terminal (`/dev/tty`), so standard output carries only the command and can be captured with `$(lfops --print-only)`.
* `--shell-init bash|zsh`: print the shell function described below.
* `--version`: print the version.


### Environment Variables

* `ESCDELAY`: milliseconds curses waits after Esc to tell it from a key sequence. Default: `25`.
* `LF_GITHUB`: the LFOps checkout is looked for in `$LF_GITHUB/lfops` if `LFOPS_DIR` is not set.
* `LF_GITLAB`: the inventories are `$LF_GITLAB/*/ans/hosts.yml` if `LFOPS_INVENTORIES` is not set. Inventory paths are shown relative to it.
* `LFOPS_DIR`: the LFOps checkout that ansible-navigator mounts as the collection. Without it and without `LF_GITHUB`, the installed collection in `~/.ansible/collections/ansible_collections/linuxfabrik/lfops` is used.
* `LFOPS_INVENTORIES`: a glob for the inventory files, for example `~/inventories/*/hosts.yml`. Empty files are skipped.
* `XDG_STATE_HOME`: the history of the entries and runs used last is kept in `$XDG_STATE_HOME/lfops/history.json`, readable by the owner only, as typed options such as `--extra-vars` may hold secrets. Default: `~/.local/state`.


### Shell Integration

Started directly, the tool runs the command right away, and only the `lfops` call ends up in the shell history. A shell function instead puts the assembled command on the prompt, where it can be edited: Enter runs it, Ctrl-C drops it. The command takes the place of the `lfops` call in the history, so it can be repeated or changed later. The function calls `command lfops`, so the tool has to be on the `PATH` under the name the function is defined for.

Bash, in `~/.bashrc` (needs bash 4.4 or newer):

```bash
eval "$(command lfops --shell-init bash)"
```

zsh, in `~/.zshrc`:

```zsh
eval "$(command lfops --shell-init zsh)"
```

Under another name, use that name in both places, for example `eval "$(command lfo --shell-init zsh)"`.

The two shells differ slightly:

* Bash shows the command on a prompt of its own (`read`), with the readline key bindings. The command is added to the history even if it is dropped with Ctrl-C, an edited command is added as well.
* zsh puts the command into the line editor buffer (`print -z`), so it appears at the next regular prompt. It ends up in the history once it runs, a dropped command does not. A `zshaddhistory` hook (registered with `add-zsh-hook`, alongside existing hooks) keeps the `lfops` call itself out of the history.
