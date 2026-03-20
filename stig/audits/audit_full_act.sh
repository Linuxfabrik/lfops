source /tmp/lib.sh
    
grep -Pq -- '^\h*disk_full_action\h*=\h*(halt|single)\b' /etc/audit/auditd.conf || exit $FAIL
grep -Pq -- '^\h*disk_error_action\h*=\h*(syslog|single|halt)\b' /etc/audit/auditd.conf || exit $FAIL

exit $PASS