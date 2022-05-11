source /tmp/lib.sh

if is_not_installed 'iptables'; then exit $FAIL; fi
exit $PASS
