source /tmp/lib.sh

if systemctl is-active --quiet rsyslog; then
  exit $PASS
fi

if systemctl is-active --quiet systemd-journald; then
  if systemd-analyze cat-config systemd/journald.conf systemd/journald.conf.d/* 2>/dev/null | grep -Eq '^Compress=yes\b'; then
    exit $PASS
  fi
  exit $FAIL
fi

exit $FAIL
