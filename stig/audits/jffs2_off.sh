source /tmp/lib.sh

check_kernel_module_disabled "jffs2" "fs" && exit $PASS || exit $FAIL
