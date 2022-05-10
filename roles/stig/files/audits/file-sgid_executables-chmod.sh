source /tmp/lib.sh

audit_lines=$(df --local -P | awk '{if (NR!=1) print $6}' | xargs -I '{}' find '{}' -xdev -type f -perm -2000 2>/dev/null)
if [ -n "$audit_lines" ]; then
    echo SGID executables
    echo ----------------
    echo ''
    echo "$audit_lines"
    echo ''
    exit $REV
fi
exit $PASS
