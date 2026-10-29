# shellcheck shell=bash
# Extracts /etc and the files of `${EXTRACT}` (space-separated absolute paths) of
# `${PACKAGE}-${VERSION}` from the RPM repository `${REPO}` to /out/root, after checking
# the package signature against `${GPG_KEY}`. All of /etc is kept, so further files of
# the same release need no second download. The package is downloaded into the
# container first, the 2 GB graylog-datanode package needs that much free space below
# ~/.local/share/containers. The install scripts and triggers go to /out/scripts.
# Builds whose release matches `${PRERELEASE_RE}` (`1.alpha.1`) are skipped, with
# `${ALLOW_PRERELEASE}` only if a final build exists: rpm sorts `7.3.0-1.alpha.1` after
# `7.3.0-1`, so `--latest-limit=1` alone would pick the pre-release (verified against
# dnf 4.14 on Rocky 9).

dnf install --assumeyes --quiet cpio >/dev/null
printf '[app]\nname=app\nbaseurl=%s\n' "${REPO}" > /etc/yum.repos.d/app.repo
# a repository can serve several architectures and the source package
releases=$(dnf --quiet --repo=app \
    repoquery --arch=noarch,x86_64 --queryformat '%{release}' "${PACKAGE}-${VERSION}" \
    | sort --unique)
if [ -z "${releases}" ]; then
    fail "${PACKAGE} ${VERSION} not found in ${REPO_DISPLAY}"
fi
final=$(awk -v pattern="${PRERELEASE_RE}" 'tolower($0) !~ pattern' <<< "${releases}")
if [ -n "${final}" ]; then
    releases=${final}
elif [ -z "${ALLOW_PRERELEASE}" ]; then
    releases=$(paste --serial --delimiters=' ' <<< "${releases}")
    fail "${PACKAGE} ${VERSION}: only pre-release builds (release ${releases})\
 in ${REPO_DISPLAY}, see --allow-prerelease"
fi
release=$(sort --version-sort <<< "${releases}" | tail --lines=1)
# `%{location}` is relative to the repository, `--location` prints the URL
url=$(dnf --quiet --repo=app \
    repoquery --arch=noarch,x86_64 --latest-limit=1 --location \
    "${PACKAGE}-${VERSION}-${release}")
get "${GPG_KEY}" --output /var/tmp/key
# a key bound with a SHA-1 signature (OpenSearch 2.x) fails to import under the default
# crypto policy: "Hash algorithm SHA1 not available" (verified against rpm 4.16 on
# Rocky 9). gpgv in fetch-deb.sh accepts it as is.
if [ -n "${GPG_SHA1}" ]; then
    update-crypto-policies --set DEFAULT:SHA1 >/dev/null
fi
rpmkeys --import /var/tmp/key
get "${url}" --output /var/tmp/package.rpm
# `rpmkeys --checksig` also succeeds for an unsigned package, it then prints `digests OK`
# (verified against rpm 4.16 on Rocky 9)
if ! rpmkeys --checksig /var/tmp/package.rpm | grep --quiet ': digests signatures OK$'; then
    fail "${PACKAGE} ${VERSION}: the package is not signed with the gpg_key"
fi
mkdir --parents /out/root
patterns=('./etc/*')
for path in ${EXTRACT}; do
    patterns+=(".${path}")
done
rpm2cpio /var/tmp/package.rpm \
    | (cd /out/root && cpio --extract --make-directories --quiet "${patterns[@]}")
rpm --query --package --scripts --triggers /var/tmp/package.rpm > /out/scripts
echo "${REPO_DISPLAY} ${url##*/}" > /out/source
