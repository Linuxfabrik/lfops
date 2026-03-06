source /tmp/lib.sh

has_mount_option /dev/shm nodev && exit $PASS || exit $FAIL
