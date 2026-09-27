#!/usr/bin/env python3
# -*- coding: utf-8; py-indent-offset: 4 -*-
#
# Author:  Linuxfabrik GmbH, Zurich, Switzerland
# Contact: info (at) linuxfabrik (dot) ch
#          https://www.linuxfabrik.ch/
# License: The Unlicense, see LICENSE file.

"""Merge hash-pinned pip-compile lockfiles into one requirements file.

Runs on the Ansible controller. Each lockfile entry is a `name==version` line followed by
indented `--hash=` and comment lines. The files are read in the order given, and an entry for
a package that an earlier file already listed replaces it, so the last file wins. Entries whose
name is passed with `--exclude` are dropped. Global option lines such as `--only-binary lxml`
are kept, each once, at the top of the result.

The monitoring-plugins lockfile resolves the dependencies of the released linuxfabrik-lib,
while the source install deploys the library from its own repository, which can be ahead of
that release. Applying the library lockfile last keeps the pins that library was tested
against, which is what the one-line installer gets with two consecutive pip calls. A single
merged file lets pip install everything in one call, so a second run changes nothing.
"""

import argparse
import re
import sys


def normalize(name):
    # PEP 503: runs of `-`, `_` and `.` are equivalent, and names are case-insensitive
    return re.sub(r'[-_.]+', '-', name).lower()


def read_entries(path, options):
    entries = {}
    current = None
    with open(path, encoding='utf-8') as f:
        for line in f:
            if not line.strip() or line.startswith('#'):
                continue
            if line[0].isspace():
                if current is not None:
                    entries[current].append(line.rstrip('\n'))
                continue
            if line.startswith('-'):
                # a global pip option, e.g. `--only-binary lxml` from requirements.in
                current = None
                if line.strip() not in options:
                    options.append(line.strip())
                continue
            match = re.match(r'([A-Za-z0-9][A-Za-z0-9._-]*)', line)
            if not match:
                sys.exit(f'{path}: cannot parse line: {line.strip()}')
            current = normalize(match.group(1))
            entries[current] = [line.rstrip('\n')]
    return entries


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        '--exclude',
        action='append',
        default=[],
        help='Package name to drop from the result. Can be given multiple times.',
    )
    parser.add_argument(
        '--output',
        required=True,
        help='File to write the merged requirements to.',
    )
    parser.add_argument(
        'lockfiles',
        nargs='+',
        help='Lockfiles in ascending precedence: the last one wins.',
    )
    args = parser.parse_args()

    merged = {}
    options = []
    for path in args.lockfiles:
        merged.update(read_entries(path, options))
    for name in args.exclude:
        merged.pop(normalize(name), None)
    if not merged:
        sys.exit('the lockfiles contain no requirements')

    with open(args.output, 'w', encoding='utf-8') as f:
        for option in options:
            f.write(option + '\n')
        for name in sorted(merged):
            f.write('\n'.join(merged[name]) + '\n')


if __name__ == '__main__':
    main()
