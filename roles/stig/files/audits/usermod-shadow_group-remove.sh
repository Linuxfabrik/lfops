source /tmp/lib.sh

shadow_gid=$(grep '^shadow:[^:]*:[^:]*:[^:]+' /etc/group)
if [ -z $shadow_gid ]; then exit $PASS; fi
audit_lines=$(awk -F: '($4 == "$shadow_gid") { print }' /etc/passwd)
if [ -n "$(echo "$audit_lines" | sed 's/\s*$//')" ]; then
    echo shadow group members
    echo --------------------
    echo ''
    echo "$audit_lines"
    echo ''
    exit $FAIL
fi
exit $PASS
