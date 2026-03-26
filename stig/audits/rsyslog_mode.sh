source /tmp/lib.sh

if systemctl is-active --quiet systemd-journald; then
  exit $PASS
fi

if systemctl is-active --quiet rsyslog; then
  if grep -Psq '^\h*\$FileCreateMode\h+0[0,2,4,6][0,2,4]0\b' /etc/rsyslog.conf /etc/rsyslog.d/*.conf 2>/dev/null; then
    exit $PASS
  fi
  exit $FAIL
fi

exit $PASS
