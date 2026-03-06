source /tmp/lib.sh

if systemctl is-active --quiet rsyslog; then
  exit $PASS
fi

if systemctl is-active --quiet systemd-journald; then
  if systemctl is-enabled systemd-journal-upload.service 2>/dev/null | grep -qx 'enabled' && \
     systemctl is-active systemd-journal-upload.service 2>/dev/null | grep -qx 'active'; then
    exit $PASS
  fi
  exit $FAIL
fi

exit $FAIL
