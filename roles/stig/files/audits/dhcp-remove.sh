source /tmp/lib.sh

if is_installed 'dhcp'; then exit $FAIL; fi
exit $PASS
