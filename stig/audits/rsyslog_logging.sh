source /tmp/lib.sh

if systemctl is-active --quiet systemd-journald; then
  exit $PASS
fi

if systemctl is-active --quiet rsyslog; then
  if [ -e /var/log/maillog ]; then
    exit $PASS
  fi
  exit $FAIL
fi

exit $PASS
