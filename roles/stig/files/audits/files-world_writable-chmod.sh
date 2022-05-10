source /tmp/lib.sh

audit_lines=$(df --local -P | awk 'NR!=1 {print $6}' | xargs -I '{}' find '{}' -xdev -type f -perm -0002 2>/dev/null)
if [ -n "$audit_lines" ]; then
    echo world writable files
    echo --------------------
    echo ''
    echo "$audit_lines"
    echo ''
    exit $FAIL
fi
exit $PASS
