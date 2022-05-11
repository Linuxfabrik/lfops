source /tmp/lib.sh

if is_enabled 'squid'; then exit $FAIL; fi
exit $PASS
