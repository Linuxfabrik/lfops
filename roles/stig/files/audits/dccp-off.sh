source /tmp/lib.sh

if is_active_kernelmod 'dccp'; then exit $FAIL; fi
exit $PASS
