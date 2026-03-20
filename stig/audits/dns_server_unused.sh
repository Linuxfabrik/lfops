source /tmp/lib.sh

service_unused 'bind' named.service && exit $PASS || exit $FAIL
