#!/usr/bin/env python3
# -*- coding: utf-8; py-indent-offset: 4 -*-
#
# Author:  Linuxfabrik GmbH, Zurich, Switzerland
# Contact: info (at) linuxfabrik (dot) ch
#          https://www.linuxfabrik.ch/
# License: The Unlicense, see LICENSE file.

"""Make this checkout importable as `ansible_collections.linuxfabrik.lfops`.

Modules and lookups import their shared code via the collection-qualified
path, e.g.

    from ansible_collections.linuxfabrik.lfops.plugins.module_utils.bitwarden import Bitwarden

For that to resolve under a plain pytest/tox run (without installing the
collection), build a temporary `ansible_collections/linuxfabrik/lfops`
tree that symlinks back to the repo and put it on sys.path. Filter and
lookup tests that load a plugin by file path do not need this, but it is
harmless for them.
"""

import os
import pathlib
import sys
import tempfile

_REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent


def _make_collection_importable():
    root = pathlib.Path(tempfile.mkdtemp(prefix='lfops_ansible_collections_'))
    link_parent = root / 'ansible_collections' / 'linuxfabrik'
    link_parent.mkdir(parents=True, exist_ok=True)
    link = link_parent / 'lfops'
    if not link.exists():
        link.symlink_to(_REPO_ROOT, target_is_directory=True)
    sys.path.insert(0, str(root))
    os.environ.setdefault('ANSIBLE_COLLECTIONS_PATH', str(root))


# make the tests/ directory importable so test modules can `import ansible_harness`
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

_make_collection_importable()
