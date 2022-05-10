source /tmp/lib.sh

if [ "$(grep -e ^\s*Storage /etc/systemd/journald.conf 2>/dev/null)" != 'Storage=persistent' ]; then exit $FAIL; fi
exit $PASS
