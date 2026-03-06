source /tmp/lib.sh

grep -Pi '^\h*LEGACY\b' /etc/crypto-policies/config >/dev/null 2>&1 && exit $FAIL
exit $PASS