source /tmp/lib.sh

check_kernel_module_disabled "udf" "fs" && exit $PASS || exit $FAIL
