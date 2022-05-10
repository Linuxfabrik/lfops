source /tmp/lib.sh

if is_installed 'squid'; then exit $FAIL; fi
exit $PASS
