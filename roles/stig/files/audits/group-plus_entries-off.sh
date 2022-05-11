source /tmp/lib.sh

audit_lines=$(grep '^\+:' /etc/group)
if [ -n "$audit_lines" ]; then
    echo Ensure no legacy "+" entries exist in /etc/group
    echo ------------------------------------------------
    echo ''
    echo "$audit_lines"
    echo ''
    exit $FAIL
fi
exit $PASS
