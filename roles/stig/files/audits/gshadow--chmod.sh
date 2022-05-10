source /tmp/lib.sh

if test_perms 000 '/etc/gshadow-'; then exit $PASS; fi
exit $FAIL
