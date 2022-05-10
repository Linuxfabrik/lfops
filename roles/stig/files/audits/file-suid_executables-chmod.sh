source /tmp/lib.sh

audit_lines=$(df --local -P | awk '{if (NR!=1) print $6}' | xargs -I '{}' find '{}' -xdev -type f -perm -4000 2>/dev/null)
if [ -n "$audit_lines" ]; then
    echo SUID executables
    echo ----------------
    echo ''
    echo "$audit_lines"
    echo ''
    exit $REV
fi
exit $PASS
