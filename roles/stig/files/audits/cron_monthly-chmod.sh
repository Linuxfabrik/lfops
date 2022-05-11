source /tmp/lib.sh

if test_perms 700 '/etc/cron.monthly'; then exit $PASS; fi
exit $FAIL
