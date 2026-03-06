source /tmp/lib.sh

has_mount_option /tmp noexec && exit $PASS || exit $FAIL
