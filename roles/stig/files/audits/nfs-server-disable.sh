source /tmp/lib.sh

if is_enabled 'nfs-server'; then exit $FAIL; fi
exit $PASS
