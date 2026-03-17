# Temporary diff helpers for ansible-freeipa modules.
# Remove once https://github.com/freeipa/ansible-freeipa/pull/1415
# is merged and released.

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

from ansible.module_utils._text import to_text


def _compare_key(arg, ipa_arg):
    """Compare a single key's value using compare_args_ipa logic."""
    if isinstance(ipa_arg, (list, tuple)):
        if not isinstance(arg, list):
            arg = [arg]
        if len(ipa_arg) != len(arg):
            return False
        if ipa_arg and arg and not (
            isinstance(ipa_arg[0], type(arg[0]))
            or isinstance(arg[0], type(ipa_arg[0]))
        ):
            arg = [to_text(_a) for _a in arg]
        try:
            return set(arg) == set(ipa_arg)
        except TypeError:
            return arg == ipa_arg
    return arg == ipa_arg


class IPADiffTracker:
    """Track before/after state for Ansible --diff output."""

    def __init__(self):
        self._diffs = []

    def build_diff(self):
        """Return kwargs for exit_json (empty dict if no changes)."""
        if not self._diffs:
            return {}
        return {"diff": self._diffs}

    def add_entry_diff(self, name, before, after):
        """Record a diff entry for one IPA object."""
        if before == after:
            return
        self._diffs.append({
            "before_header": name,
            "after_header": name,
            "before": before,
            "after": after,
        })


def gen_args_diff(args, res_find, ignore=None):
    """Extract only changed keys from args vs res_find for diff output.

    Returns (before_dict, after_dict) containing only keys that differ.
    Uses the same comparison logic as compare_args_ipa for consistency.
    Single-element IPA lists are normalized to scalars for readability.
    """
    if not args:
        return {}, {}
    before = {}
    after = {}
    if ignore is None:
        ignore = []
    for key in args:
        if key in ignore:
            continue
        arg = args[key]
        ipa_arg = res_find.get(key, [""])
        if not _compare_key(arg, ipa_arg):
            # Normalize for display
            _ipa = ipa_arg[0] if isinstance(ipa_arg, (list, tuple)) \
                and len(ipa_arg) == 1 else ipa_arg
            _arg = arg[0] if isinstance(arg, (list, tuple)) \
                and len(arg) == 1 else arg
            before[key] = _ipa
            after[key] = _arg
    return before, after


def gen_member_diff(member_key, add_list, del_list, current_list):
    """Compute before/after for one member category.

    Returns (before_dict, after_dict) with member_key as key and sorted
    lists as values. Returns ({}, {}) if no changes.
    """
    if not add_list and not del_list:
        return {}, {}
    current = sorted(current_list or [])
    desired = sorted(
        [x for x in current if x not in (del_list or [])]
        + (add_list or [])
    )
    return {member_key: current}, {member_key: desired}


def merge_diffs(*diff_pairs):
    """Merge multiple (before, after) tuples into a single pair."""
    merged_before = {}
    merged_after = {}
    for _before, _after in diff_pairs:
        merged_before.update(_before)
        merged_after.update(_after)
    return merged_before, merged_after
