source /tmp/lib.sh

if is_active_kernelmod 'udf'; then exit $FAIL; fi
exit $PASS
