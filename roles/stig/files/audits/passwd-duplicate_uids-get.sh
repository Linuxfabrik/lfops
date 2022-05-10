source /tmp/lib.sh

audit_lines=$(cut -f3 -d: /etc/passwd | sort | uniq --count | awk '$1 > 1')
if [ -n "$(echo "$audit_lines" | sed 's/\s*$//')" ]; then
    echo duplicate UIDs
    echo --------------
    echo ''
    echo "$audit_lines"
    echo ''
    exit $FAIL
fi
exit $PASS
