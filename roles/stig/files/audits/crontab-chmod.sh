source /tmp/lib.sh

if test_perms 600 '/etc/crontab'; then exit $PASS; fi
exit $FAIL
