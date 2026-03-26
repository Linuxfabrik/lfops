source /tmp/lib.sh

has_mount_option /tmp nodev && exit $PASS || exit $FAIL
