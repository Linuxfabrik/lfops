source /tmp/lib.sh

if is_installed 'mcstrans'; then exit $FAIL; fi
exit $PASS
