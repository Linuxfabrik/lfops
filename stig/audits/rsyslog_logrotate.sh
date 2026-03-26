source /tmp/lib.sh

if systemctl is-active --quiet systemd-journald; then
  exit $PASS
fi

if systemctl is-active --quiet rsyslog; then
  l_output="" l_rotate_conf=""
  if [ -f /etc/logrotate.conf ]; then
    l_rotate_conf="/etc/logrotate.conf"
  elif compgen -G "/etc/logrotate.d/*.conf" >/dev/null 2>&1; then
    for file in /etc/logrotate.d/*.conf; do
      l_rotate_conf="$file"
    done
  else
    l_output="$l_output\n- rsyslog is in use and logrotate is not configured"
  fi

  if [ -z "$l_output" ]; then
    exit $PASS
  fi
  exit $FAIL
fi

exit $PASS
