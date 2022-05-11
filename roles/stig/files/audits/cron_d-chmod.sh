source /tmp/lib.sh

if test_perms 700 '/etc/cron.d'; then exit $PASS; fi
exit $FAIL
