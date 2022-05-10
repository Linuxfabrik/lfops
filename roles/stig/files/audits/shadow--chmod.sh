source /tmp/lib.sh

if test_perms 000 '/etc/shadow-'; then exit $PASS; fi
exit $FAIL
