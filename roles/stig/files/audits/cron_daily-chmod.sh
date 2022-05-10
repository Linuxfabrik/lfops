source /tmp/lib.sh

if test_perms 700 '/etc/cron.daily'; then exit $PASS; fi
exit $FAIL
