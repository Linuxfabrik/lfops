source /tmp/lib.sh

if is_installed 'cups'; then exit $FAIL; fi
exit $PASS
