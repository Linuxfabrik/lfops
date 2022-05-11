source /tmp/lib.sh

if is_enabled 'avahi-daemon'; then exit $FAIL; fi
exit $PASS
