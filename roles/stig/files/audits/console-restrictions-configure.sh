source /tmp/lib.sh

if [ ! -e /etc/securetty ]; then exit $FAIL; fi
audit_lines=$(cat /etc/securetty)
if [ -n "$audit_lines" ]; then
    echo Ensure root login is restricted to system console
    echo -------------------------------------------------
    echo ''
    echo "$audit_lines"
    echo ''
    exit $REV
fi
exit $PASS
