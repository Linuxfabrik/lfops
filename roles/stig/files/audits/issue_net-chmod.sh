source /tmp/lib.sh

if test_perms 644 '/etc/issue.net'; then exit $PASS; fi
exit $FAIL
