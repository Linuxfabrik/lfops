source /tmp/lib.sh

if is_enabled 'dhcpd'; then exit $FAIL; fi
exit $PASS
