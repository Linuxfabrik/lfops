source /tmp/lib.sh

audit_lines=$(grep -E '^\s*auth\s+required\s+pam_faillock.so\s+' /etc/pam.d/password-auth /etc/pam.d/system-auth 2>/dev/null)
echo pam-password lockout configuration
echo ----------------------------------
echo ''
if [ -n "$audit_lines" ]; then
    echo "$audit_lines"
    echo ''
    exit $REV
else
    echo "No rules found."
    echo ''
    exit $FAIL
fi
