source /tmp/lib.sh

audit_lines=$(for dir in $(awk -F: '{ print $6 }' /etc/passwd | sort | uniq); do
        if [ -e "$dir/.rhosts" ]; then echo "$dir/.rhosts"; fi
    done)
if [ -n "$(echo "$audit_lines" | sed 's/\s*$//')" ]; then
    echo Ensure no users have .rhosts files
    echo ----------------------------------
    echo ''
    echo "$audit_lines"
    echo ''
    exit $FAIL
fi
exit $PASS
