---
name: lfops-follow-upstream
description: Update LFOps after an upstream application release, e.g. a `follow-upstream: <app> <version>` GitHub issue, a newreleases.io notice ("New Graylog2/graylog2-server releases"), a pasted release mail, or "Graylog 7.3.0 is out". Merges the packaged configuration changes into the versioned templates, adds templates for a new release series, and prepares the CHANGELOG entry and commit message. Use when a release notice or a new upstream version is mentioned.
---

# LFOps follow upstream

Brings the LFOps templates in line with a new upstream release. The deterministic part (fetching the packaged files, the three-way merge, header and supported-versions bookkeeping) is done by `tools/follow-upstream`; this skill covers what the tool cannot judge. Work from the repository root. Never commit: end with a report and a proposed commit message. The only exception is a headless run of the follow-upstream timer, whose prompt says what it may commit.


## 1. Collect the releases

Take the releases from whatever the user provides:

* `<app> <version>` as arguments.
* A GitHub issue titled `follow-upstream: <app> <version>`, opened by the `Linuxfabrik: Follow upstream` workflow. Use the title only, and remember the issue number for the pull request (step 6).
* A pasted mail or text: extract upstream project and versions. A newreleases.io mail lists them as `Graylog2/graylog2-server on GitHub ...` followed by `- 7.2.1` lines. Matomo instances send "New Matomo 5.14.0 is available".
* Nothing: list the open issues with `gh issue list --label follow-upstream --state open`. None: ask what was released.

Ignore pre-releases (`alpha`, `beta`, `rc`, `-dev`). A plain version number is no proof of a final release: some vendors keep the marker in the package release only (Graylog ships 7.3.0-alpha.1 as `graylog-server-7.3.0-1.alpha.1`).


## 2. Triage every release

The repository is the state, not the mail: a release already covered needs no work, however often it is reported.

* Find the application in `tools/follow-upstream.yml` by its `upstream` names.
* Not listed: check whether a role deploys the application at all (`grep -ril <name> roles/*/README.md`). No role: report "not used by LFOps" and move on. A role exists: report it as a candidate for `tools/follow-upstream.yml` and ask before adding it (see "Adding an application").
* Listed: run `tools/follow-upstream <app> <version>`, oldest release first. It fetches the RPM and the DEB of the release, checks their signatures and caches them, so expect a few GB of downloads for large packages. Exit code 0: nothing to review, 1: findings or conflicts, 2: the run aborted.
* `packaging:` lines come first. Each one means upstream changed how it packages the application: a file below /etc that is neither templated nor ignored, a templated file the release no longer ships, a file that differs between RPM and DEB, or install scripts that differ from those of the base release in more than the version (an install script that modifies the packaged file on the host would be reverted by the template). Do not resolve these yourself, and do not accept the merge of that release: stop and report them, with the `diff` the tool prints. Whether the role needs a new template, a per-format template or an `ignore` entry is the user's decision.
* A failed fetch (`not found in`) aborts the run. Upstream may have published one format before the other; report it and retry later rather than merging without the check.
* `only pre-release builds` aborts the run as well: the release is not final yet. Stop and report it, do not rerun with `--allow-prerelease`, that is the user's decision. The same applies if the GitHub project of the application has only pre-release tags for the version (`7.3.0-alpha.1`, but no `7.3.0`), even if the run succeeded. No commit in either case.
* Then one line per template:
    * `already covers`: nothing to do.
    * `is identical in`: the packaged file did not change, the tool only updated the `Based on` line. Commit it anyway (step 6), so `tools/follow-upstream --check` stops reporting the release.
    * `merged cleanly` / `N conflict(s)`: continue with step 3.
    * `no "Based on <package> <version>" line`: see "Bootstrapping a template".
    * A new release series (template created from the latest older one): also step 4.


## 3. Review the merge

For every changed template, read the upstream diff the tool prints (`diff <base> <new>`) and the release notes / upgrade notes of the release.

* Resolve conflict markers (`<<<<<<<`). Keep the LFOps change (role variables, Jinja logic, security defaults) and take the upstream text around it.
* New upstream option: leave it as shipped (usually commented out). Only propose a role variable if an administrator plausibly needs it, and ask first.
* Removed or renamed upstream option that a role variable feeds: stop and ask. Renaming or dropping a role variable is a breaking change of the public interface.
* Changed upstream default that a role default overrides: report it.
* Do not reformat, re-wrap or "fix" upstream text. Templates stay as close to the packaged file as possible.
* `copies` in `tools/follow-upstream.yml` receive the same merge result; check that they still match their target platform.


## 4. New release series

The tool created `<series>-<file>.j2` from the latest older template and added the series to `supported_versions`.

* Fix every line the tool lists as still mentioning the old series (e.g. a `go2docs.graylog.org/7-1/` link).
* Check the role for other places that enumerate versions: README (`grep -n <old series> roles/<role>/README.md`), `meta/argument_specs.yml` choices, related `repo_*` roles.
* Read the upgrade notes for breaking changes, required migration steps and dropped platforms. Report them; they may need tasks, preflight checks or a `Breaking Changes` entry.
* Check whether a series has gone EOL upstream. Dropping a series is a separate decision for the user (CONTRIBUTING: "Do not support EOL software versions").


## 5. Test

* Run the Molecule scenario that covers the role if one exists (`grep -rl <role> extensions/molecule/*/converge.yml`), per CONTRIBUTING.md "Testing". Report it if there is none.
* Check for leftover conflict markers: `grep -rn '^<<<<<<<\|^>>>>>>>' roles/<role>/templates`.


## 6. Changelog and commit message

Follow CONTRIBUTING.md "Changelog" and "Changelog Sections", and the existing entries:

* Patch release inside an existing series: no CHANGELOG entry (the deployed file only gains upstream comments). Commit: `chore(roles/<role>): sync the <series> <file> template with <App> <version>`, the body names what upstream changed.
* New series: entry under `### Added` of `## [Unreleased]`, at the top: `* **role:<role>, role:<role>**: Add template for <App> <series>.` Commit: `feat(roles/<role>, roles/<role>): add template for <App> <series>`.
* A change an administrator has to act on: `### Breaking Changes` or `### Changed`, as CONTRIBUTING.md describes.
* Only the `Based on` line changed (`is identical in`): no CHANGELOG entry, the line does not end up on the host. Commit: `chore(roles/<role>): record that the <series> <file> template covers <App> <version>`.
* Releases from a `follow-upstream` issue: the pull request body gets one `Closes #<number>` line per issue, so merging it into `main` closes them.


## 7. Report

Per release: what was done or why nothing was, conflicts and how they were resolved, open questions, test result, proposed commit message(s). An issue whose release is already covered on `main` (`already covers`): say so, it can be closed by hand.


## Bootstrapping a template

`tools/follow-upstream` needs `{# Based on <package> <version> #}` below the version line of the template header. The Jinja comment does not end up in the deployed file, so adding it changes nothing on the hosts and needs no timestamp bump. To find the version:

1. Fetch the packaged file of the candidate releases of the series (the tool caches them under `~/.cache/lfops-follow-upstream/rpm/<app>/<package>-<version>/root/`, `deb/` for an entry with `format: 'deb'`). The upstream git tree under `~/git/other` is a good first filter, but packages may rewrite the file (Graylog sets absolute paths), so confirm against the package.
2. Diff each against the template (skipping the header). The release with the fewest differing lines is the base. Where several releases ship an identical file, take the newest.
3. Add the line and rerun the tool.


## Adding an application

Add an entry to `tools/follow-upstream.yml` (format in its header comment). Only for templates that are copies of a packaged file; a drop-in written from scratch has no base. `tools/follow-upstream` needs both a Yum and an APT repository serving every release of a series; an application packaged only for one family, or only by the distributions, needs the tool extended first. Run the tool once for the current release and put every reported file LFOps does not template into `ignore`, after checking that no role deploys it. Read the install scripts of the current release (`scripts` next to `root` in the cache) and note in a comment above the entry how they treat the templated files, with the release you checked (`grafana 13.2.4: postinst copies the samples unchanged`); later releases only report changes to them.
