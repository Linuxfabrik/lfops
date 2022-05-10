source /tmp/lib.sh

if [ "$(grep -e ^\s*Compress /etc/systemd/journald.conf 2>/dev/null)" != 'Compress=yes' ]; then exit $FAIL; fi
exit $PASS
