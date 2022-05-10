source /tmp/lib.sh

if is_not_installed 'sudo'; then exit $FAIL; fi
exit $PASS
