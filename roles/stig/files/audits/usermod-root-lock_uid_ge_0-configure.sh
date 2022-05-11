source /tmp/lib.sh

audit_lines=$(awk -F: '$3 == 0 {print$1}' /etc/passwd)
if [ "$audit_lines" != 'root' ]; then
    echo Ensure root is the only UID 0 account
    echo -------------------------------------
    echo ''
    echo "$audit_lines"
    echo ''
    exit $FAIL
fi
exit $PASS
