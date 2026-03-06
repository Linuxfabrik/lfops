source /tmp/lib.sh

has_mount_option /var/tmp nosuid && exit $PASS || exit $FAIL
