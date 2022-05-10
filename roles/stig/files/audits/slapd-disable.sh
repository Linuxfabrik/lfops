source /tmp/lib.sh

if is_enabled 'slapd'; then exit $FAIL; fi
exit $PASS
