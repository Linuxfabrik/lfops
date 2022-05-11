source /tmp/lib.sh

audit_lines=$(awk -F: '($2 == "" )' /etc/shadow)
if [ -n "$audit_lines" ]; then
    echo Ensure password fields are not empty
    echo ------------------------------------
    echo ''
    echo "$audit_lines"
    echo ''
    exit $REV
fi
exit $PASS
