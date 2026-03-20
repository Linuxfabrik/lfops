source /tmp/lib.sh

check_kernel_module_disabled "squashfs" "fs" && exit $PASS || exit $FAIL
