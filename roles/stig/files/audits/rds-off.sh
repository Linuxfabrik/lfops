source /tmp/lib.sh

if is_active_kernelmod 'rds'; then exit $FAIL; fi
exit $PASS
