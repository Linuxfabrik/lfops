source /tmp/lib.sh

check_kernel_module_disabled "freevxfs" "fs" && exit $PASS || exit $FAIL
