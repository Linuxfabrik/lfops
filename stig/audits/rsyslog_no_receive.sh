source /tmp/lib.sh

# 6.2.3.7 rsyslog not configured to receive logs (no imtcp) (only if rsyslog is used)
if systemctl is-active --quiet systemd-journald; then
  exit $PASS
fi

if systemctl is-active --quiet rsyslog; then
  if grep -Psi -- '^\h*module\(load=\"?imtcp\"?\)' /etc/rsyslog.conf /etc/rsyslog.d/*.conf 2>/dev/null | grep -q .; then
    exit $FAIL
  fi
  if grep -Psi -- '^\h*input\(type=\"?imtcp\"?\b' /etc/rsyslog.conf /etc/rsyslog.d/*.conf 2>/dev/null | grep -q .; then
    exit $FAIL
  fi
  #obsolete legacy format:
  if grep -Psi -- '^\h*\$ModLoad\h+imtcp\b' /etc/rsyslog.conf /etc/rsyslog.d/*.conf 2>/dev/null | grep -q .; then
    exit $FAIL
  fi
  if grep -Psi -- '^\h*\$InputTCPServerRun\b' /etc/rsyslog.conf /etc/rsyslog.d/*.conf 2>/dev/null | grep -q .; then
    exit $FAIL
  fi
  exit $PASS
fi

exit $PASS
