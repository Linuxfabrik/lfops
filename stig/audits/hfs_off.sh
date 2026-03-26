source /tmp/lib.sh

check_kernel_module_disabled "hfs" "fs" && exit $PASS || exit $FAIL
