source /tmp/lib.sh

if [ "$(getenforce)" == 'Disabled' ]; then exit $SKIP; fi

audit_lines=$(getsebool -a | grep httpd_ | grep ' on')
if [ -n "$audit_lines" ]; then
    echo check enabled selinux booleans
    echo ------------------------------
    echo ''
    echo "$audit_lines"
    echo ''
fi

exit $REV
