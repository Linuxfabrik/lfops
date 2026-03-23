source /tmp/lib.sh

has_mount_option /home nodev && exit $PASS || exit $FAIL
