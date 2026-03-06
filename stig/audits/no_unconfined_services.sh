source /tmp/lib.sh

if ! ps -eZ | grep -q 'unconfined_service_t'; then
  exit $FAIL
fi
exit $PASS