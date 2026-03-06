source /tmp/lib.sh

has_mount_option /home nosuid && exit $PASS || exit $FAIL
