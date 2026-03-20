source /tmp/lib.sh

has_mount_option /var/log nosuid && exit $PASS || exit $FAIL
