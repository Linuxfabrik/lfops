source /tmp/lib.sh

if is_installed 'talk'; then exit $FAIL; fi
exit $PASS
