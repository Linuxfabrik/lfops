source /tmp/lib.sh

check_kernel_module_disabled "usb-storage" "drivers" && exit $PASS || exit $FAIL
