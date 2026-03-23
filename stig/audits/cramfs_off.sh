source /tmp/lib.sh

check_kernel_module_disabled "cramfs" "fs" && exit $PASS || exit $FAIL
