source /tmp/lib.sh

if is_installed 'bind'; then exit $FAIL; fi
exit $PASS
