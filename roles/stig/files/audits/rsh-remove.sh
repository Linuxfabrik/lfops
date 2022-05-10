source /tmp/lib.sh

if is_installed 'rsh'; then exit $FAIL; fi
exit $PASS
