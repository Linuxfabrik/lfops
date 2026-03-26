source /tmp/lib.sh

has_mount_option /var/log/audit nodev && exit $PASS || exit $FAIL
