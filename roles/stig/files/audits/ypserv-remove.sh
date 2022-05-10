source /tmp/lib.sh

if is_installed 'ypserv'; then exit $FAIL; fi
exit $PASS
