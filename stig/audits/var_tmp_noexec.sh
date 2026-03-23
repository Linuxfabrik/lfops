source /tmp/lib.sh

has_mount_option /var/tmp noexec && exit $PASS || exit $FAIL
