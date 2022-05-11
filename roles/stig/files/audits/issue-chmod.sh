source /tmp/lib.sh

if test_perms 644 '/etc/issue'; then exit $PASS; fi
exit $FAIL
