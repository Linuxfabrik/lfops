source /tmp/lib.sh

service_unused 'ypserv' ypserv.service && exit $PASS || exit $FAIL
