source /tmp/lib.sh

has_mount_option /var/log noexec && exit $PASS || exit $FAIL
