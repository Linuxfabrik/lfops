source /tmp/lib.sh

if test_perms 644 '/etc/group'; then exit $PASS; fi
exit $FAIL
