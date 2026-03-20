source /tmp/lib.sh

if is_active 'systemd-journald'; then
  exit $PASS
fi

if is_active 'rsyslog'; then
  if is_enabled 'rsyslog'; then
    exit $PASS
  fi
  exit $FAIL
fi

exit $PASS
