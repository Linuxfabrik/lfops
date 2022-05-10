source /tmp/lib.sh
source /tmp/lib-apache-httpd.sh

audit_lines=$(find $APACHE_PREFIX -path $APACHE_PREFIX/htdocs -path /var/www -prune -o \! -group root -ls)
if [ -n "$audit_lines" ]; then
    echo files in the Apache directory that are not owned by group root
    echo --------------------------------------------------------------
    echo ''
    echo "$audit_lines"
    echo ''
    exit $FAIL
fi
exit $PASS
