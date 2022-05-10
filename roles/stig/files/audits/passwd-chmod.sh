source /tmp/lib.sh

if test_perms 644 '/etc/passwd'; then exit $PASS; fi
exit $FAIL
