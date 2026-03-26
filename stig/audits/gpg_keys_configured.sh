source /tmp/lib.sh

if grep -r gpgkey /etc/yum.repos.d/* /etc/dnf/dnf.conf >/dev/null 2>&1 && is_installed 'gpg-pubkey'; then
  exit $PASS
fi
exit $FAIL
