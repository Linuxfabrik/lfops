source /tmp/lib.sh

if [ $(grep -E --count '^max_log_file\s*=\s*[0-9]*' /etc/audit/auditd.conf) -eq 1 ]; then exit $PASS; fi
exit $FAIL
