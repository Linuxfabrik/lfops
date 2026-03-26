source /tmp/lib.sh

has_separate_partition /var && exit $PASS || exit $FAIL
