source /tmp/lib.sh

has_mount_option /tmp nosuid && exit $PASS || exit $FAIL
