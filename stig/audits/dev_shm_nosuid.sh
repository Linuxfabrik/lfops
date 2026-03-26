source /tmp/lib.sh

has_mount_option /dev/shm nosuid && exit $PASS || exit $FAIL
