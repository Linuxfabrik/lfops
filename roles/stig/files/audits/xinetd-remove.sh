source /tmp/lib.sh

if is_installed 'xinetd'; then exit $FAIL; fi
exit $PASS
