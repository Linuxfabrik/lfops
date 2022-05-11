source /tmp/lib.sh

if is_enabled 'lighttpd'; then exit $FAIL; fi
exit $PASS
