source /tmp/lib.sh

if is_not_installed 'firewalld'; then exit $FAIL; fi
exit $PASS
