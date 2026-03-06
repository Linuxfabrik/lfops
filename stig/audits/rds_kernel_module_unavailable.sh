source /tmp/lib.sh

check_kernel_module_disabled "rds" "net" && exit $PASS || exit $FAIL
