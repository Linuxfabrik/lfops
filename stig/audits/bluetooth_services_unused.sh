source /tmp/lib.sh

service_unused 'bluez' bluetooth.service && exit $PASS || exit $FAIL
