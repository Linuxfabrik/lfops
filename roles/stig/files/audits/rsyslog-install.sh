source /tmp/lib.sh

if is_installed 'rsyslog'; then exit $PASS; fi
exit $FAIL
