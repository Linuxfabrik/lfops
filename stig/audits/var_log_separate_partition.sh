source /tmp/lib.sh

has_separate_partition /var/log && exit $PASS || exit $FAIL
