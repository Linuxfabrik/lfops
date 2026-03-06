source /tmp/lib.sh

has_separate_partition /home && exit $PASS || exit $FAIL
