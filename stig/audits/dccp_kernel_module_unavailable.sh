source /tmp/lib.sh

check_kernel_module_disabled "dccp" "net" && exit $PASS || exit $FAIL
