source /tmp/lib.sh

if grep -Po -- '^\h*max_log_file\h*=\h*\d+\b' /etc/audit/auditd.conf > /dev/null; then
    exit $PASS
else
    exit $FAIL
fi
