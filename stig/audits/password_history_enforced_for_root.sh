source /tmp/lib.sh

grep -Pi -- '^\h*enforce_for_root\b' /etc/security/pwhistory.conf >/dev/null 2>&1 || exit $FAIL

exit $PASS