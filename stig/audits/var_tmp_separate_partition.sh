source /tmp/lib.sh

has_separate_partition /var/tmp && exit $PASS || exit $FAIL
