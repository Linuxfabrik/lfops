source /tmp/lib.sh

if is_enabled 'cups'; then exit $FAIL; fi
exit $PASS
