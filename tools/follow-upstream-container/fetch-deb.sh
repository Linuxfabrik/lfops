# shellcheck shell=bash
# Extracts /etc of `${PACKAGE}` `${VERSION}` from the APT repository `${REPO}` to
# /out/root, see fetch-rpm.sh. Checks the chain apt checks: the signature of InRelease
# against `${GPG_KEY}`, the checksum of the Packages index listed there, and the checksum
# of the package listed in the index. The index can list several builds of a release
# (`7.2.0-1`, `7.2.0-11`); the newest one wins, as with `dnf repoquery --latest-limit=1`.

dnf install --assumeyes --quiet bsdtar >/dev/null
get "${GPG_KEY}" --output /var/tmp/key
if grep --quiet 'BEGIN PGP' /var/tmp/key; then
    gpg --batch --quiet --dearmor --output /var/tmp/key.gpg /var/tmp/key
else
    mv /var/tmp/key /var/tmp/key.gpg
fi
get "${REPO}/dists/${SUITE}/InRelease" --output /var/tmp/InRelease
if ! gpgv --keyring /var/tmp/key.gpg --output /var/tmp/Release /var/tmp/InRelease \
    2>/dev/null; then
    fail "${PACKAGE} ${VERSION}: InRelease is not signed with the gpg_key"
fi
index="${COMPONENT}/binary-amd64/Packages.gz"
sum=$(awk -v path="${index}" '
    /^[^ ]/ { section = $1 }
    section == "SHA256:" && $3 == path { print $1 }' /var/tmp/Release)
get "${REPO}/dists/${SUITE}/${index}" --output /var/tmp/Packages.gz
if [ -z "${sum}" ] \
    || ! echo "${sum}  /var/tmp/Packages.gz" | sha256sum --check --status; then
    fail "${PACKAGE} ${VERSION}: the checksum of ${index} does not match InRelease"
fi
line=$(gunzip --stdout /var/tmp/Packages.gz \
    | awk -v package="${PACKAGE}" -v version="${VERSION}" '
        BEGIN { RS = ""; FS = "\n" }
        {
            name = ""; ver = ""; file = ""; sum = ""
            for (i = 1; i <= NF; i++) {
                if ($i ~ /^Package: /) name = substr($i, 10)
                if ($i ~ /^Version: /) ver = substr($i, 10)
                if ($i ~ /^Filename: /) file = substr($i, 11)
                if ($i ~ /^SHA256: /) sum = substr($i, 9)
            }
            sub(/^[0-9]+:/, "", ver)
            if (name == package && (ver == version || index(ver, version "-") == 1))
                print ver, file, sum
        }' \
    | sort --version-sort | tail --lines=1)
read -r _ file sum <<< "${line}"
if [ -z "${file:-}" ]; then
    fail "${PACKAGE} ${VERSION} not found in ${REPO_DISPLAY}"
fi
get "${REPO}/${file}" --output /var/tmp/package.deb
if [ -z "${sum:-}" ] \
    || ! echo "${sum}  /var/tmp/package.deb" | sha256sum --check --status; then
    fail "${PACKAGE} ${VERSION}: the checksum of ${file##*/} does not match the index"
fi
mkdir --parents /out/root
bsdtar --extract --to-stdout --file /var/tmp/package.deb 'data.tar*' \
    | (cd /out/root && bsdtar --extract --file - --include './etc/*' --include 'etc/*')
echo "${REPO_DISPLAY} ${file##*/}" > /out/source
