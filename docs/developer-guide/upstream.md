# Following Upstream Releases

Templates that are copies of a packaged file (`<series>-coolwsd.xml.j2`, `<series>-server.conf.j2`, ...) have to follow the configuration changes of every upstream release. `tools/follow-upstream.yml` lists these applications: their package repositories, the templates built from each packaged file, and the `supported_versions` list a new series goes into. The format is described in its header.

* The `Linuxfabrik: Follow upstream` workflow runs `tools/follow-upstream --check` every weekday. For each release newer than the `Based on` lines it opens an issue titled `follow-upstream: <app> <version>` with the label `follow-upstream`. Applications whose repository needs a customer token are checked outside the CI, where the token is available; their issues look the same.
* The pull request that brings LFOps up to date lists one `Closes #<number>` per issue. A closed issue means LFOps is ready for that release.
* `tools/follow-upstream <app> <version>` does the work: it fetches the RPM and the DEB of the release, checks their signatures, extracts `/etc` and the templated files outside of it, compares the packaging (new or vanished files, RPM and DEB differing, changed install scripts), and merges the upstream changes into every template with `git merge-file`, keeping the LFOps changes. A new release series gets a new template from the newest older one and is added to `supported_versions`. Conflicts are left as conflict markers. `--dry-run` writes nothing, `--list <app>` lists the releases in the repositories, `--check` lists what needs work. Packages are cached in `~/.cache/lfops-follow-upstream/`.
* The `lfops-follow-upstream` skill covers what the tool cannot judge: resolving conflicts, upgrade notes of a new series, the CHANGELOG entry and the commit message.
* A release whose packaged file did not change only updates the `Based on` line. Commit it anyway, without a CHANGELOG entry, so `--check` stops reporting the release and its issue gets closed.
* A patch release inside an existing series needs no CHANGELOG entry, a new series goes under `### Added`.


## Workarounds and Planned Removals

Code that is only there until something happens elsewhere (a workaround for an upstream bug, a branch for a platform until its end of life, a vendored copy of an upstream module) gets an entry in `tools/maintenance.yml`, in the same pull request. The format is described in its header.

* Write `done_when` and `check` so that someone else can decide without your context: name the upstream issue, the release or commit that has to be in, and how to verify it (`git tag --contains`, a package version in a container). A closed issue is not enough.
* Point to the entry from the code with a comment that names the upstream link (e.g. `# see https://github.com/Icinga/icinga2/issues/10617`), or the `id` of the entry if there is no upstream link, so `git grep` finds every place.
* The pull request that removes the workaround removes the entry.
* The `lfops-maintenance` skill runs the checks of all due entries and reports which ones need work. It runs from a recurring calendar reminder.


## Vendored Plugins

Some plugins are vendored from upstream (local patches, upstream needs a newer ansible-core, or the dependency must ship to the managed node). Keep them in lockstep with upstream; re-sync or drop them when the condition is met.

* `plugins/modules/ipagroup.py`, `ipahbacrule.py`, `ipahostgroup.py`, `ipapwpolicy.py`, `ipasudocmd.py`, `ipasudocmdgroup.py`, `ipasudorule.py`, `ipauser.py`: from <https://github.com/freeipa/ansible-freeipa>, with `--diff` support from PR [#1415](https://github.com/freeipa/ansible-freeipa/pull/1415). Drop when a release contains it; switch to `freeipa.ansible_freeipa.<module>`.
* `plugins/modules/lvm_pv.py`: from community.general (PR [#10070](https://github.com/ansible-collections/community.general/pull/10070), in 11.0.0, which needs ansible-core >= 2.18; LFOps still supports RHEL 8 / Python 3.6). Local patches, keep on re-sync: `from __future__ import annotations` replaced by `from __future__ import absolute_import, division, print_function`, and `pvresize` only runs when the device holds more or fewer extents than the PV (`pv_needs_resize()`), since every `pvresize` writes a file to `/etc/lvm/archive`. `rescan_device()` is taken from upstream commit 6f22759f (PR [#13218](https://github.com/ansible-collections/community.general/pull/13218), fixing [#13212](https://github.com/ansible-collections/community.general/issues/13212)), which is newer than the rest of the file; take it as is on re-sync. Drop when LFOps requires ansible-core >= 2.18; switch to `community.general.lvm_pv` and update `roles/lvm`.
* `plugins/module_utils/gnupg.py` (with `gnupg.py_LICENSE.txt`): byte-identical [python-gnupg](https://github.com/vsajip/python-gnupg), revision in its `__version__`, used by `gpg_key` on the managed node to avoid a pip install there. Not expected to be dropped; re-sync unmodified.
