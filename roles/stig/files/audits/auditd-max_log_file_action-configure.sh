source /tmp/lib.sh

if [ $(grep --count '^max_log_file_action\s*=\s*keep_logs' /etc/audit/auditd.conf) -eq 1 ]; then exit $PASS; fi
exit $FAIL
