source /tmp/lib.sh
source /tmp/lib-apache-httpd.sh

if [ -z "$APACHE_CONF" ]; then
    echo "http://localhost/server-info not found or does not return any data"
    exit $FAIL
fi

# unfortunately not specific for the Web Root Directory, but better than to check nothing
conf=$(echo "$APACHE_CONF" | grep -i ";Options " | grep -iE '(None|Multiviews)')
if [ -z "$conf" ]; then
    exit $FAIL
fi

exit $REV
