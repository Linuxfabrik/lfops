# shellcheck shell=bash
# Extracts /etc of `${PACKAGE}-${VERSION}` from the RPM repository `${REPO}` to /out/root,
# after checking the package signature against `${GPG_KEY}`. All of /etc is kept, so
# further files of the same release need no second download. The package is downloaded
# into the container first, the 2 GB graylog-datanode package needs that much free space
# below ~/.local/share/containers.

dnf install --assumeyes --quiet cpio >/dev/null
printf '[app]\nname=app\nbaseurl=%s\n' "${REPO}" > /etc/yum.repos.d/app.repo
# a repository can serve several architectures and the source package
url=$(dnf --quiet --repo=app \
    repoquery --arch=noarch,x86_64 --latest-limit=1 --location "${PACKAGE}-${VERSION}")
if [ -z "${url}" ]; then
    fail "${PACKAGE} ${VERSION} not found in ${REPO_DISPLAY}"
fi
get "${GPG_KEY}" --output /var/tmp/key
rpmkeys --import /var/tmp/key
get "${url}" --output /var/tmp/package.rpm
# `rpmkeys --checksig` also succeeds for an unsigned package, it then prints `digests OK`
# (verified against rpm 4.16 on Rocky 9)
if ! rpmkeys --checksig /var/tmp/package.rpm | grep --quiet ': digests signatures OK$'; then
    fail "${PACKAGE} ${VERSION}: the package is not signed with the gpg_key"
fi
mkdir --parents /out/root
rpm2cpio /var/tmp/package.rpm \
    | (cd /out/root && cpio --extract --make-directories --quiet "./etc/*")
echo "${REPO_DISPLAY} ${url##*/}" > /out/source
