source /tmp/lib.sh

has_mount_option /var/log/audit noexec && exit $PASS || exit $FAIL
