source /tmp/lib.sh

if is_active_kernelmod 'squashfs'; then exit $FAIL; fi
exit $PASS
