source /tmp/lib.sh
source /tmp/lib-apache-httpd.sh

if [ -z "$APACHE_CONF" ]; then
    echo "http://localhost/server-info not found or does not return any data"
    exit $FAIL
fi

conf=$(echo "$APACHE_CONF" | grep -i "/etc/httpd/conf.d/welcome.conf")
if [ -n "$conf" ]; then
    exit $FAIL
fi

# here, there could be searched for more on other OS's

exit $REV
