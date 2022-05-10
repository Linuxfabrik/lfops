source /tmp/lib.sh

if is_enabled 'rsyslog'; then exit $PASS; fi
exit $FAIL
