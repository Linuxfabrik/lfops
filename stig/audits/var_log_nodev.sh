source /tmp/lib.sh

has_mount_option /var/log nodev && exit $PASS || exit $FAIL
