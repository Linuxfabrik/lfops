source /tmp/lib.sh

if is_active_kernelmod 'tipc'; then exit $FAIL; fi
exit $PASS
