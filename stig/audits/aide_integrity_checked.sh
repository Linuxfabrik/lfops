source /tmp/lib.sh

cron_hits="$(grep -Ers '^([^#]+\s+)?(\/usr\/s?bin\/|^\s*)aide(\.wrapper)?\s(--?\S+\s)*(--(check|update)|\$AIDEARGS)\b' /etc/cron.* /etc/crontab /var/spool/cron/ 2>/dev/null)"

if [ -z "$cron_hits" ]; then
    exit $FAIL
fi

exit $PASS