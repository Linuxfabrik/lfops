source /tmp/lib.sh

check_kernel_module_disabled "sctp" "net" && exit $PASS || exit $FAIL
