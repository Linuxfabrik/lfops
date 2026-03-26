source /tmp/lib.sh

service_unused 'cups' cups.socket cups.service && exit $PASS || exit $FAIL
