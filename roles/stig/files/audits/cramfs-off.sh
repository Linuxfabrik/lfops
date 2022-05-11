source /tmp/lib.sh

if is_active_kernelmod 'cramfs'; then exit $FAIL; fi
exit $PASS
