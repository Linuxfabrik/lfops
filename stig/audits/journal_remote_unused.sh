source /tmp/lib.sh

if systemctl is-active --quiet rsyslog; then
  exit $PASS
fi

if systemctl is-active --quiet systemd-journald; then
  if systemctl is-enabled systemd-journal-remote.socket systemd-journal-remote.service 2>/dev/null | grep -Pq '^enabled'; then
    exit $FAIL
  fi
  if systemctl is-active systemd-journal-remote.socket systemd-journal-remote.service 2>/dev/null | grep -Pq '^active'; then
    exit $FAIL
  fi
  exit $PASS
fi

exit $FAIL
