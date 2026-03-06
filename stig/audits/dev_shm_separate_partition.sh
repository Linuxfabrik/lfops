source /tmp/lib.sh

has_separate_partition /dev/shm && exit $PASS || exit $FAIL
