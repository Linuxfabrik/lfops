source /tmp/lib.sh

if [ "$(getenforce)" == 'Disabled' ]; then exit $SKIP; fi
if [ -n "$(ps -eZ | grep unconfined_service_t)" ]; then exit $FAIL; fi
exit $PASS
