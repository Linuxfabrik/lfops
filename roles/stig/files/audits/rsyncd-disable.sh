source /tmp/lib.sh

if is_enabled 'rsyncd'; then exit $FAIL; fi
exit $PASS
