source /tmp/lib.sh
source /tmp/lib-apache-httpd.sh

audit_lines=$(find $APACHE_PREFIX \! -user root -ls)
if [ -n "$audit_lines" ]; then
    echo files in the Apache directory that are not owned by user root
    echo -------------------------------------------------------------
    echo ''
    echo "$audit_lines"
    echo ''
    exit $FAIL
fi
exit $PASS
