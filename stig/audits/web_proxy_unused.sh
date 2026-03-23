source /tmp/lib.sh

service_unused 'squid' squid.service && exit $PASS || exit $FAIL
