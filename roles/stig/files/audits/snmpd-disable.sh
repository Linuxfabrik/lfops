source /tmp/lib.sh

if is_enabled 'snmpd'; then exit $FAIL; fi
exit $PASS
