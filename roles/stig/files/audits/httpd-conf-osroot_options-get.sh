source /tmp/lib.sh
source /tmp/lib-apache-httpd.sh

if [ -z "$APACHE_CONF" ]; then
    echo "http://localhost/server-info not found or does not return any data"
    exit $FAIL
fi

conf=$(echo "$APACHE_CONF" | grep -i ";Options ")
if [ -z "$conf" ]; then
    # directive was not set at all
    exit $FAIL
fi

# in all other cases, a manual review is needed
exit $REV
