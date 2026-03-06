source /tmp/lib.sh

has_mount_option /var nosuid && exit $PASS || exit $FAIL
