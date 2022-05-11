source /tmp/lib.sh

if is_installed 'telnet-server'; then exit $FAIL; fi
exit $PASS
