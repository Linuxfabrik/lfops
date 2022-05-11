source /tmp/lib.sh

if is_enabled 'ypserv'; then exit $FAIL; fi
exit $PASS
