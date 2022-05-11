source /tmp/lib.sh
source /tmp/lib-apache-httpd.sh

audit_lines=$(find -L $APACHE_PREFIX \! -type l -perm /o=w -ls)
if [ -n "$audit_lines" ]; then
    echo files in the Apache directory that are owned by others
    echo ------------------------------------------------------
    echo ''
    echo "$audit_lines"
    echo ''
    exit $FAIL
fi
exit $PASS
