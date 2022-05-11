source /tmp/lib.sh

if is_installed 'telnet'; then exit $FAIL; fi
exit $PASS
