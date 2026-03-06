source /tmp/lib.sh

has_separate_partition /var/log/audit && exit $PASS || exit $FAIL
