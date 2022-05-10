source /tmp/lib.sh

if is_not_installed 'aide'; then exit $FAIL; fi
exit $PASS
