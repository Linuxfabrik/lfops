source /tmp/lib.sh

has_mount_option /dev/shm noexec && exit $PASS || exit $FAIL
