source /tmp/lib.sh

if [ $(grep -Rl 'aide' /var/spool/cron/root /etc/cron* 2>/dev/null | wc -l) -eq 1 ]; then exit $PASS; fi
if [ $(systemctl list-timers | grep 'aide' 2>/dev/null | wc -l) -eq 1 ]; then exit $PASS; fi
exit $FAIL
