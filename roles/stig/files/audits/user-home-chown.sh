source /tmp/lib.sh

audit_lines=$(awk -F: '{ print $1 " " $3 " " $6 }' /etc/passwd | while read user uid dir; do
    if [ $uid -ge 1000 -a -d "$dir" -a $user != "nfsnobody" ]; then
        owner=$(stat -L -c "%U" "$dir")
        if [ "$owner" != "$user" ]; then echo "$dir: owner=$owner, user=$user"; continue; fi
    fi
done)
if [ $(echo "$audit_lines" | wc -l) -ne 1 ]; then
    echo home directories and their owners
    echo ---------------------------------
    echo ''
    echo "$audit_lines"
    echo ''
    exit $FAIL
fi
exit $PASS
