source /tmp/lib.sh

if is_enabled 'nginx'; then exit $FAIL; fi
exit $PASS
