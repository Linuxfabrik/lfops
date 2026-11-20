# Testing

Molecule tests the playbooks (and thereby the roles) in `extensions/molecule`. When you change a role or playbook, update its scenario in the same step: new or changed behaviour into `verify.yml`, changed inputs (renamed or new variables, other defaults) into its `inventory`.

* `<playbook>/` (e.g. `apps/`), optionally with sub-scenarios (`install/`, `remove/`): `converge.yml` runs the playbook, `verify.yml` checks the result, `molecule.yml` (required, may override `config.yml`, e.g. VM vs container), `inventory/` (`hosts.yml` puts shared-inventory hosts into the playbook's group, `group_vars/systems_under_test.yml` holds the variables).
* `config.yml` applies to all scenarios; `default/` is unused but required; `inventory/` is the shared inventory (`hosts.yml` required); `playbooks/` holds the provisioning playbooks.
* `example/` is the fully commented reference scenario; copy it for a new test.
* To cover `--check`, put Molecule's `check` step before `converge` into the scenario's `test_sequence`, and build the starting point in the scenario's own `prepare.yml`, which `check` then sees (reference: `extensions/molecule/acme_sh`). A play with `check_mode: true` is no substitute: its tasks run in check mode, but `ansible_check_mode` stays `false`, since ansible-core sets it from `--check` only (verified with ansible-core 2.16), so guards on it are never exercised.
* A role's checks go into the scenario of its own playbook (create it if missing), not into `setup_basic` or another scenario that merely runs the role.
* A scenario that deploys the Linuxfabrik Monitoring Plugins tests their latest release, never a pinned one: it imports `playbooks/monitoring-plugins-latest.yml` in its `converge.yml` (see `extensions/molecule/setup_basic`). A pin goes stale unnoticed and hides problems of the release the hosts actually get.


## Preparing the controller

* **Collection path**: the scenarios import playbooks by FQCN, so symlink the checkout, from the very directory you run `molecule` in: `ln --symbolic --no-target-directory --force "$(pwd)" ~/.ansible/collections/ansible_collections/linuxfabrik/lfops`. For several worktrees see "Running scenarios in parallel".
* **`libvirt` group** membership; VM provisioning does not escalate.
* **Storage pool** in a directory no package owns, not the distribution's `default` pool (package upgrades reset its mode, and a `chmod` rewrites the ACL mask, so the grant decays to `#effective:--x` and `qemu-img` fails with `Permission denied`):

    ```bash
    sudo mkdir --parents /var/lib/libvirt/images-lfops-molecule
    sudo chown "$(id -un):$(id -gn)" /var/lib/libvirt/images-lfops-molecule
    sudo chmod 0751 /var/lib/libvirt/images-lfops-molecule  # qemu only traverses
    # SELinux; restorecon has no long options
    sudo semanage fcontext --add --type virt_image_t '/var/lib/libvirt/images-lfops-molecule(/.*)?'
    sudo restorecon -R -v /var/lib/libvirt/images-lfops-molecule
    sudo virsh pool-define-as lfops-molecule dir --target /var/lib/libvirt/images-lfops-molecule
    sudo virsh pool-autostart lfops-molecule
    sudo virsh pool-start lfops-molecule
    # keeps cached base images replaceable after libvirt chowns them to qemu
    setfacl --default --modify "user:$(id -un):rw" /var/lib/libvirt/images-lfops-molecule
    ```

    `lfops-molecule` is the expected name (`LFOPS_TEST_POOL` selects another). `create` re-fetches a newer rolling `latest` cloud image only while the pool holds no boot disk, so `--destroy=never` keeps images pinned. Delete images from before the `setfacl` once. Never run `virsh pool-build` on it, and keep it outside your home (qemu cannot traverse a `0700` home).
* **libvirt network `default`** (check with `virsh --connect qemu:///system net-list --all`): `sudo virsh net-define /usr/share/libvirt/networks/default.xml`, then `net-autostart default` and `net-start default`. If `virbr0` or `192.168.122.0/24` are taken, define it from a copy edited with `sed --expression="s/name='virbr0'/name='virbr1'/" --expression='s/192\.168\.122\./192.168.123./g'`.


## Running a scenario

Run `molecule test --scenario-name apps/install` from the repository root with Molecule 26+. Otherwise `config.yml` is not read (or, measured with 25.12, sub-scenario names are not resolved), and the scenario "passes" against an empty inventory.

* `LFOPS_TEST_TARGETS='rocky*'`: comma-separated subset of targets (`localhost` is always included); also scopes `molecule destroy` to rebuild one target, keeping the SSH keypair and inventory of the others.
* `LFOPS_TEST_POOL`: storage pool, default `lfops-molecule`.
* `LFOPS_TEST_ID`: see "Running scenarios in parallel".

`molecule test` destroys the instances at the end, also on failure; `--destroy=never` keeps them for inspection. There is no leading `destroy`, so the next run reuses them. Remove them with `molecule destroy --scenario-name apps/install`.

Whole suite, each scenario independently, skipping `default` and `example` (`bash` and `zsh`):

```bash
failed=()
while IFS= read -r scenario; do
    echo "### ${scenario}"
    molecule test --scenario-name "${scenario}" || failed+=("${scenario}")
done < <(find extensions/molecule -name molecule.yml -printf '%P\n' \
    | sed 's#/molecule.yml$##' \
    | grep --invert-match --extended-regexp '^(default|example(/|$))' \
    | sort)
[ "${#failed[@]}" -eq 0 ] && echo 'All scenarios passed.' || printf 'FAILED: %s\n' "${failed[@]}"
```


## Running scenarios in parallel

Parallel runs (e.g. two worktrees) need, opt-in:

* **A collection path per worktree**, kept in the shell that runs `molecule` (e.g. `direnv`). Prerun then logs `Found symlinked collection, skipping its installation`; `requirements.yml` collections are installed into the worktree on the first run.

    ```bash
    export ANSIBLE_HOME="$(pwd)/.ansible"
    mkdir --parents "${ANSIBLE_HOME}/collections/ansible_collections/linuxfabrik"
    ln --symbolic --no-target-directory --force "$(pwd)" \
        "${ANSIBLE_HOME}/collections/ansible_collections/linuxfabrik/lfops"
    ```

* **Own instance names** via `LFOPS_TEST_ID='pr248'`: `rocky9-vm` becomes `lfops-molecule-pr248-rocky9-vm` with its own boot disk, so one run's `destroy` does not take the other's VMs. `molecule destroy` only removes instances of the given `LFOPS_TEST_ID`. The pool is shared on purpose.


## Known Limitations

* `libvirt` group membership is root-equivalent, and owning the pool adds filesystem write access; no reduction over passwordless sudo, only explicit. `qemu:///session` is not usable, since address discovery needs the `default` network of `qemu:///system`.
* Not usable inside an Ansible Execution Environment: provisioning acts on the host's libvirt, podman and pool directory from `localhost`.


## How a scenario runs

The `test_sequence` in `config.yml`: `dependency` (collections from `requirements.yml`), `create` (VMs or containers), `prepare` (wait, gather facts), `converge`, `verify`, `idempotence` (second run, fails on any change), `verify` again, `destroy`.


## What to verify

Verify what only the running system can confirm, not the role's steps. An assertion that still passes while the service is dead or misconfigured tests the wrong thing.

* Do not re-check what comes for free: a failing playbook fails `converge`, and `idempotence` checks the second run.
* Do **not** assert that a templated file exists or contains a line, nor make "the package is installed" the goal (a one-line smoke check is fine).
* Do assert that the service runs and is enabled (`ansible.builtin.service_facts`), is reachable (`ansible.builtin.wait_for` or a request), and actually *uses* the configured values: ask it (`ansible.builtin.uri` against an API, or a CLI printing the effective configuration) for the value set in `group_vars`. Also assert end state outside packages and files (users, databases, API objects), or its absence in a removal scenario.


## Warnings fail a scenario

A warning in `converge`, `idempotence` or `verify` fails the scenario, since it usually means a task does not do what it is meant to on some platform (a `find` on a path that does not exist there, a deprecated parameter). Molecule itself only looks at the exit code of `ansible-playbook`, and `verify.yml` does not see the warnings of `converge`, so `config.yml` loads the callback `extensions/molecule/callback_plugins/lfops_fail_on_warnings.py`. It collects every warning while `converge.yml` or `verify.yml` runs, lists the ones no allowlist accepts at the end, and makes `ansible-playbook` exit with `1`.

* Fix the cause, do not hide the warning. Accept it only if the role cannot avoid it, with an entry in `extensions/molecule/warnings-allowlist.yml` (all scenarios) or in `warnings-allowlist.yml` next to the `molecule.yml` of the scenario. Each entry has a `pattern` (Python regex, searched in the text with whitespace collapsed) and a mandatory `reason`.
* What a warning on screen does not tell you, and why `verify.yml` is the wrong place to look for one:

    * Ansible shows a text only once per run (`Display._warns`), so a warning missing on screen may have occurred again. The callback sees every one.
    * In a loop, ansible-core moves the warnings of the items to the result of the task (`executor/task_executor.py`) and drops them from `results[*]`. An `assert` on `result["results"][*]["warnings"]` always passes.
    * ansible-core 2.19+ hands warnings to the main process as a `WarningSummary` (`Display._warning`), before that `Display.warning` itself is proxied from the workers. The callback hooks whichever exists, verified with ansible-core 2.16, 2.18 and 2.22.

* Not covered: deprecation warnings, and warnings issued before the callbacks are loaded (inventory parsing, `ansible-galaxy` in the `dependency` step), as well as `create`, `prepare` and `destroy`.
* A callback cannot set the exit code of `ansible-playbook`, and an exception raised in it is swallowed before ansible-core 2.19, or keeps the callbacks after it from finishing. So the callback changes a zero exit code on the way out (`sys.exit`). An exit code that already signals a failure is kept.


## Troubleshooting

**Prerun aborts with `ansible_compat.errors.InvalidPrerequisiteError: Command ansible-galaxy collection install -vvv --force /path/to/lfops`**: `galaxy.yml` carries the non-semver `version: main`. Either set `prerun: false` top-level in `config.yml` and install LFOps yourself, or make the collection symlink (under `ANSIBLE_HOME`) resolve to the directory you run `molecule` in.


## Why libvirt VMs and Podman containers, and not microVMs

libkrun microVMs (`podman run --runtime=krun`) were evaluated and not adopted: `podman exec` into them fails ([crun#2090](https://github.com/containers/crun/issues/2090)), they run libkrun's kernel instead of the distro's, and init images exist only for the Red Hat family. systemd as PID 1 works with `KRUN_INIT_PID1=1`. Revisit if crun#2090 lands.
