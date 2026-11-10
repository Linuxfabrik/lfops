---
name: lfops-maintenance
description: Run the recurring LFOps maintenance checks from `tools/maintenance.yml`, e.g. "run the maintenance checks", "Wartungsarbeiten", "what workarounds can we drop?", or the monthly calendar reminder. Checks every due entry (workarounds waiting for an upstream fix or release, distribution and ansible-core end of life, vendored code to re-sync, scanning alerts) and reports which entries need work. Changes no code.
---

# LFOps maintenance

`tools/maintenance.yml` lists work that becomes due at some point: workarounds that wait for an upstream fix or release, code kept for a platform until its end of life, vendored code to re-sync, and periodic chores. This skill checks which entries are due and reports. It changes no code, opens no pull request and never commits; the work itself is an ordinary task the user starts afterwards. Work from the repository root.


## 1. Select the entries

* Read `tools/maintenance.yml`.
* An entry is due if `not_before` has passed (or is unset) and `last_checked` is unset or older than its `interval` (`monthly`: 28 days, `quarterly`: 84 days).
* The user can name entries or ask for all of them; then ignore `interval` and `not_before`.


## 2. Run the checks

* Run the `check` of each due entry as written. Independent checks can run in parallel.
* The check decides, not the issue state: a closed issue or a merged pull request is no fix until a release contains it, and a fixed release only counts once it is the minimum LFOps supports (`done_when`). Verify with `git tag --contains`, the release list or the package version in a container, as the entry says.
* Fetch upstream source to `~/git/other/<project>` if a check needs it.
* A check that cannot run (API error, missing tool, ambiguous result) is reported as failed with the reason, never guessed.
* Verify that the files in `where` still exist and still contain the workaround (`git grep` the `id` or the upstream link). An entry whose workaround is gone is reported as stale.


## 3. Look for unlisted workarounds

`git grep` for comments that name an upstream issue or pull request (`github.com/.../issues/`, `/pull/`, `jira.`, `bugzilla`) or say `workaround` / `hotfix`, outside `CHANGELOG.md`. Report hits that no entry covers, as candidates. Skip text copied from upstream config files into templates.


## 4. Report

One block per outcome, most actionable first:

* **Due**: `done_when` holds. Name the entry, the evidence (release, tag, date) and the `action`.
* **Failed**: the check could not run, with the reason.
* **Stale**: the workaround is gone, the entry can be removed.
* **Unchanged**: one line per entry with the current state, e.g. "milestone 2.17.0 still open".
* **Candidates**: unlisted workarounds from step 3.

Then propose the `last_checked` / `last_result` updates for every checked entry as a diff to `tools/maintenance.yml`, and a commit message such as `chore(tools/maintenance): record the 2026-12 checks`. Do not apply or commit it without the user's OK.
