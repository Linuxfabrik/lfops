source /tmp/lib.sh

audit_lines=$(grep -E -v '^(halt|sync|shutdown|nfsnobody)' /etc/passwd | awk -F: '($7!="/sbin/nologin" && $7!="/usr/sbin/nologin" && $7!="/bin/false") { print $1 " " $6 }' | while read -r user dir; do
    if [ ! -d "$dir" ]; then
        echo $user
    fi
done)
if [ -n "$(echo "$audit_lines" | sed 's/\s*$//')" ]; then
    echo missing users\' home directories
    echo -------------------------------
    echo ''
    echo "$audit_lines"
    echo ''
    exit $FAIL
fi
exit $PASS
