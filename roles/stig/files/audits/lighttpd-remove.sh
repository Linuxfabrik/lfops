source /tmp/lib.sh

if is_installed 'lighttpd'; then exit $FAIL; fi
exit $PASS
