source /tmp/lib.sh

if is_enabled 'auditd'; then exit $PASS; fi
exit $FAIL
