source /tmp/lib.sh

check_kernel_module_disabled "tipc" "net" && exit $PASS || exit $FAIL
