source /tmp/lib.sh

if is_installed 'ypbind'; then exit $FAIL; fi
exit $PASS
