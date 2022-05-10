source /tmp/lib.sh

if is_installed 'net-snmp'; then exit $FAIL; fi
exit $PASS
