source /tmp/lib.sh

if is_enabled 'autofs'; then exit $FAIL; fi
exit $PASS
