source /tmp/lib.sh

audit_lines=$(for dir in $(awk -F: '{ print $6 }' /etc/passwd | sort | uniq); do
        if [ -e "$dir/.forward" ]; then echo "$dir/.forward"; fi
    done)
if [ -n "$(echo "$audit_lines" | sed 's/\s*$//')" ]; then
    echo Ensure no users have .forward files
    echo -----------------------------------
    echo ''
    echo "$audit_lines"
    echo ''
    exit $FAIL
fi
exit $PASS
