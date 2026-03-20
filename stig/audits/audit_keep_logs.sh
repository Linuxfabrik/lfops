source /tmp/lib.sh

fail=0

grep -P -- '^\h*disk_full_action\h*=\h*(halt|single)\b' /etc/audit/auditd.conf >/dev/null 2>&1 || fail=1
grep -P -- '^\h*disk_error_action\h*=\h*(syslog|single|halt)\b' /etc/audit/auditd.conf >/dev/null 2>&1 || fail=1

if [ "$fail" -eq 0 ]; then
  exit $PASS
else
  exit $FAIL
fi
