source /tmp/lib.sh

if is_installed 'avahi-autoipd'; then exit $FAIL; fi
if is_installed 'avahi'; then exit $FAIL; fi
exit $PASS
