source /tmp/lib.sh

if is_enabled 'iptables'; then exit $PASS; fi
exit $FAIL
