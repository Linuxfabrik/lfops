# Plugins

In-house plugins live in `plugins/{callback,filter,lookup,modules,module_utils}/`.

* Start with the standard Linuxfabrik Python header (copy it from any in-house plugin), followed by `from __future__ import absolute_import, division, print_function` and `__metaclass__ = type`.
* Modules start with `#!/usr/bin/python` instead of the header's `#!/usr/bin/env python3`. ansible-core applies interpreter discovery and `ansible_python_interpreter` only to a shebang whose interpreter is named `python`; it runs `#!/usr/bin/env python3` as it is, which fails on RHEL 8 hosts without `python3`. The `module-shebang` pre-commit hook guards this.
* Use single quotes and f-strings (vendored plugins keep their upstream style).
* Carry valid-YAML `DOCUMENTATION` (and `RETURN` / `EXAMPLES` where applicable). A `description` bullet with a colon followed by a space becomes a mapping and breaks `ansible-doc`; rephrase or quote it. Verify with `ansible-doc --type <callback|filter|lookup|module> linuxfabrik.lfops.<name>`; `tests/unit/test_plugin_docs.py` guards this.
* Set `version_added` to the first release, never change it.
* `module_utils` holds shared code. Do not import the Linuxfabrik Python Libraries (`lib`); copy what you need and note the origin.


## Plugin Tests

Unit tests are **mandatory** for every in-house plugin; a pull request adding or changing a plugin adds or updates its test.

* `tests/unit/` mirrors the plugin tree, `test_<plugin>.py` (e.g. `tests/unit/plugins/filter/test_combine_lod.py`). Plugins with collection-qualified imports are imported via `ansible_collections.linuxfabrik.lfops...`, which `tests/conftest.py` makes resolvable. Assert behavior, not implementation details.
* Controller plugins (`callback/`, `filter/`, `lookup/`) run on the controller's Python (>= 3.10). Managed-node plugins (`modules/`, `module_utils/`) must work down to Python 3.6 (RHEL 8); their tests also run in UBI 8 (`[testenv:py36-target]`), so test code must be valid Python 3.6 too.
* Run with `tox`, `tox -e py311-ansible216`, `tox -f py311` or `pytest tests/unit`, see `tests/README.md`. The `Linuxfabrik: Unit Tests` workflow runs both tiers on every push and pull request.
