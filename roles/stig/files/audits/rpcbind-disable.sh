source /tmp/lib.sh

if is_enabled 'rpcbind'; then exit $FAIL; fi
exit $PASS
