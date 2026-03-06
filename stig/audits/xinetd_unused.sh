source /tmp/lib.sh

service_unused 'xinetd' xinetd.service && exit $PASS || exit $FAIL
