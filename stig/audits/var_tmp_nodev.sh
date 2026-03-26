source /tmp/lib.sh

has_mount_option /var/tmp nodev && exit $PASS || exit $FAIL
