source /tmp/lib.sh

if ! has_usb_devices; then exit $SKIP; fi
if has_fsopt_on_usb nosuid; then exit $PASS; fi
exit $FAIL
