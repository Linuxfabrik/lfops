source /tmp/lib.sh

if [ "$(grep -e ^\s*ForwardToSyslog /etc/systemd/journald.conf 2>/dev/null)" != 'ForwardToSyslog=yes' ]; then exit $FAIL; fi
exit $PASS
