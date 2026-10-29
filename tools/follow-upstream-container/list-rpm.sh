# shellcheck shell=bash
# Lists the name, version and release of every build of `${PACKAGES}` in each repository
# of `${REPOS}` (lines of `<key> <url>`), prefixed with the key. A repository that does
# not exist (yet), e.g. the one of the next release series, yields no line instead of an
# error.

i=0
while read -r key repo; do
    i=$((i + 1))
    printf '[app%s]\nname=app\nbaseurl=%s\nskip_if_unavailable=1\n' "${i}" "${repo}" \
        > "/etc/yum.repos.d/app${i}.repo"
    # PACKAGES is a space-separated list of package names, split on purpose
    # shellcheck disable=SC2086
    dnf --quiet --repo="app${i}" \
        repoquery --arch=noarch,x86_64 --queryformat '%{name} %{version} %{release}' \
        ${PACKAGES} \
        | sed "s/^/${key} /"
done <<< "${REPOS}"
