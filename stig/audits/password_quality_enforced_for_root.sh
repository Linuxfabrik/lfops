source /tmp/lib.sh

grep -Psi -- '^\h*enforce_for_root\b' \
  /etc/security/pwquality.conf /etc/security/pwquality.conf.d/*.conf >/dev/null 2>&1 || exit $FAIL

exit $PASS