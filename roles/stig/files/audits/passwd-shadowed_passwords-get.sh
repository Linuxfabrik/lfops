source /tmp/lib.sh

audit_lines=$(awk -F: '($2 != "x" ) { print $1 " is not set to shadowed passwords "}' /etc/passwd)
if [ -n "$audit_lines" ]; then
    echo accounts in /etc/passwd that does not use shadowed passwords
    echo ------------------------------------------------------------
    echo ''
    echo "$audit_lines"
    echo ''
    exit $FAIL
fi
exit $PASS
