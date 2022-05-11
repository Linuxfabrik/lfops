source /tmp/lib.sh

audit_lines=$(cut -f1 -d: /etc/group | sort | uniq --count | awk '$1 > 1')
if [ -n "$(echo "$audit_lines" | sed 's/\s*$//')" ]; then
    echo duplicate group names
    echo ---------------------
    echo ''
    echo "$audit_lines"
    echo ''
    exit $FAIL
fi
exit $PASS
