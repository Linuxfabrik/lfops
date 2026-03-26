source /tmp/lib.sh

check_kernel_module_disabled "hfsplus" "fs" && exit $PASS || exit $FAIL
