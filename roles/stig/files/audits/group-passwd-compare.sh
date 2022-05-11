source /tmp/lib.sh

audit_lines=$(for i in $(cut -s -d: -f4 /etc/passwd | sort -u ); do
        grep -q -P "^.*?:[^:]*:$i:" /etc/group
        if [ $? -ne 0 ]; then
            echo "$i"
        fi
    done)
if [ -n "$(echo "$audit_lines" | sed 's/\s*$//')" ]; then
    echo groups that exist in /etc/passwd, but not in /etc/group
    echo -------------------------------------------------------
    echo ''
    echo "$audit_lines"
    echo ''
    exit $FAIL
fi
exit $PASS
