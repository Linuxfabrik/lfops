# Tests

Unit tests for the in-house LFOps plugins under `plugins/`.

## Two tiers

LFOps plugins run in two different environments, so they are tested differently:

| Tier | Plugins | Runs on | Python / ansible-core |
|---|---|---|---|
| Controller | `plugins/filter/`, `plugins/lookup/` | Ansible controller | Python >= 3.10, ansible-core 2.15 - latest |
| Managed node | `plugins/modules/`, `plugins/module_utils/` | target host | down to Python 3.6 (RHEL 8) |

Filter and lookup plugins are evaluated on the controller during templating, so they only ever see the controller's Python. Modules and module utils are shipped to and executed on the managed node, which on RHEL 8 still uses the system Python 3.6.

## Layout

Tests mirror the plugin tree:

```
tests/unit/plugins/filter/test_<name>.py
tests/unit/plugins/lookup/test_<name>.py
tests/unit/plugins/modules/test_<name>.py        # managed-node tier
tests/unit/plugins/module_utils/test_<name>.py   # managed-node tier
```

Each test loads its plugin by path (the plugins are not an importable package) and may import `ansible.errors` / `ansible.module_utils`, so ansible-core must be installed in the test environment.

## Running

Run the controller matrix (Python x ansible-core combinations) with tox:

```bash
tox
```

Run a single environment, or everything for one Python:

```bash
tox -e py311-ansible216
tox -f py311
```

Run the tests directly against the active interpreter (needs `pytest`, `pyyaml` and `ansible-core`):

```bash
pytest tests/unit
```

## Managed-node tier (Python 3.6 / RHEL 8)

CI runners no longer ship Python 3.6, so module tests have to run inside a RHEL 8 / UBI 8 container. The `[testenv:py36-target]` env in `tox.ini` is scaffolded for this but not yet enabled, since the only plugin with tests so far (`combine_lod`) is a controller-side filter. Enable it once module tests exist, for example:

```bash
podman run --rm -v "$PWD":/src:Z -w /src registry.access.redhat.com/ubi8/ubi \
  bash -c 'dnf -y install python3 python3-pip && pip3 install tox && tox -e py36-target'
```
