source /tmp/lib.sh

if is_enabled 'named'; then exit $FAIL; fi
exit $PASS
