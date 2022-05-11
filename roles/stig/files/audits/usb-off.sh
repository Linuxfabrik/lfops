source /tmp/lib.sh

if is_active_kernelmod 'usb-storage'; then exit $FAIL; fi
exit $PASS
