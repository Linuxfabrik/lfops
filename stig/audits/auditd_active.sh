source /tmp/lib.sh

if is_enabled 'auditd' && is_active 'auditd'; then
  exit $PASS
fi
exit $FAIL
