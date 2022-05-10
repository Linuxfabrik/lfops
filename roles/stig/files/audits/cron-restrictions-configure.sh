source /tmp/lib.sh

if [ -f /etc/cron.deny ]; then exit $FAIL; fi
if [ -f /etc/cron.allow ]; then
    if [ "$(stat /etc/cron.allow 2>/dev/null| grep -m1 ^Access:)" != 'Access: (0600/-rw-------)  Uid: (    0/    root)   Gid: (    0/    root)' ]; then exit $FAIL; fi
else
    exit $FAIL
fi
exit $PASS
