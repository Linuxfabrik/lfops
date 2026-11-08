# -*- coding: utf-8; py-indent-offset: 4 -*-
#
# Author:  Linuxfabrik GmbH, Zurich, Switzerland
# Contact: info (at) linuxfabrik (dot) ch
#          https://www.linuxfabrik.ch/
# License: The Unlicense, see LICENSE file.

"""Let a Molecule converge, idempotence or verify run fail on an Ansible warning.

Not part of the collection: extensions/molecule/config.yml loads it for the Molecule
scenarios only.
"""

DOCUMENTATION = r"""
name: lfops_fail_on_warnings
type: aggregate
short_description: Fail a Molecule converge, idempotence or verify run on a warning
description:
  - Collects every warning Ansible issues while it runs C(converge.yml) or
    C(verify.yml), and makes ansible-playbook exit with a non-zero code at the end if
    one of them is not in an allowlist.
  - The allowlists are C(extensions/molecule/warnings-allowlist.yml) and
    C(warnings-allowlist.yml) in the directory of the scenario.
requirements:
  - Enabled in extensions/molecule/config.yml (callbacks_enabled).
"""

import multiprocessing
import os
import re
import sys

import yaml
from ansible.plugins.callback import CallbackBase

# playbooks whose warnings count; idempotence runs converge.yml again
_CHECKED_PLAYBOOKS = ('converge.yml', 'verify.yml')
_ALLOWLIST_NAME = 'warnings-allowlist.yml'
# the exit code ansible-core uses for a generic error
_EXIT_CODE = 1


def _load_allowlist(path):
    """Return a list of compiled patterns. Each entry needs a `pattern` and a
    `reason`, so that no warning is accepted without saying why.
    """
    if not path or not os.path.isfile(path):
        return []
    with open(path, encoding='utf-8') as allowlist_file:
        entries = yaml.safe_load(allowlist_file) or []
    patterns = []
    for entry in entries:
        if (
            not isinstance(entry, dict)
            or not entry.get('pattern')
            or not entry.get('reason')
        ):
            raise ValueError(
                f'{path}: every entry needs a "pattern" and a "reason": {entry!r}'
            )
        patterns.append(re.compile(entry['pattern']))
    return patterns


class CallbackModule(CallbackBase):
    CALLBACK_VERSION = 2.0
    CALLBACK_TYPE = 'aggregate'
    CALLBACK_NAME = 'lfops_fail_on_warnings'
    CALLBACK_NEEDS_ENABLED = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._active = False
        self._warnings = []
        project_dir = os.environ.get('MOLECULE_PROJECT_DIRECTORY', '')
        scenario_dir = os.environ.get('MOLECULE_SCENARIO_DIRECTORY', '')
        self._allowlist = _load_allowlist(
            os.path.join(project_dir, 'extensions', 'molecule', _ALLOWLIST_NAME)
        ) + _load_allowlist(
            scenario_dir and os.path.join(scenario_dir, _ALLOWLIST_NAME)
        )

        # Display is a singleton, so patching it sees every warning, also those that
        # Display then suppresses because the same text was shown before in this run,
        # and those of Ansible itself (templating, lookups, the plugin loader).
        # Module warnings get there too: the stdout callback hands them to it
        # (CallbackBase._handle_warnings), in a loop with the result of the whole task.
        # ansible-core 2.19+ sends the warnings of the worker processes to the main
        # process as a WarningSummary through Display._warning(). Before that,
        # Display.warning() itself is proxied from the workers to the main process.
        if hasattr(type(self._display), '_warning'):
            self._orig_warning = self._display._warning
            self._display._warning = self._warning_summary_hook
        else:
            self._orig_warning = self._display.warning
            self._display.warning = self._warning_hook

    def _warning_hook(self, msg, *args, **kwargs):
        # ansible-core before 2.19
        if multiprocessing.parent_process() is None:
            self._record(msg)
        return self._orig_warning(msg, *args, **kwargs)

    def _warning_summary_hook(self, warning, *args, **kwargs):
        # ansible-core 2.19+
        if multiprocessing.parent_process() is None:
            self._record(warning.event.msg)
        return self._orig_warning(warning, *args, **kwargs)

    def _record(self, msg):
        if not self._active:
            return
        text = ' '.join(str(msg).split())
        if text in self._warnings:
            return
        if any(pattern.search(text) for pattern in self._allowlist):
            return
        self._warnings.append(text)

    def v2_playbook_on_start(self, playbook):
        self._active = os.path.basename(playbook._file_name) in _CHECKED_PLAYBOOKS

    def v2_playbook_on_stats(self, _stats):
        if not self._warnings:
            return
        lines = [
            f'lfops_fail_on_warnings: {len(self._warnings)} warning(s) not in an'
            f' allowlist ({_ALLOWLIST_NAME}), failing the run:'
        ] + [f'  - {text}' for text in self._warnings]
        self._display.display('\n'.join(lines), color='bright red', stderr=True)
        # A callback cannot set the exit code of ansible-playbook, and an exception
        # raised here would be swallowed (ansible-core before 2.19) or would keep the
        # callbacks after this one from seeing the stats. So the exit code is changed on
        # the way out: the CLI ends with sys.exit(exit_code) once the run is complete.
        # An exit code that already signals a failure is kept.
        orig_exit = sys.exit

        def _exit(code=0):
            orig_exit(_EXIT_CODE if code in (0, None) else code)

        sys.exit = _exit
