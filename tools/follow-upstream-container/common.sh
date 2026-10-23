# shellcheck shell=bash
# Put in front of every script of this directory by tools/follow-upstream, which runs
# them in a podman container. The variables come from the container environment.

set -o errexit -o nounset -o pipefail

# URLs are passed to curl through stdin and to dnf through a repository file, never as
# arguments, so a repository token does not show up in the process list. Every dnf call
# needs `--quiet`: without it, dnf prints the repository URL, token included, on an
# unreachable or missing repository (verified against dnf 4.14 on Rocky 9).
# `curl --silent --show-error` prints no URL on errors (curl 7.76).
get() {
    printf 'url = "%s"\n' "$1" | curl --fail --silent --show-error --location --config - "${@:2}"
}

fail() {
    echo "$1" >&2
    exit 1
}
