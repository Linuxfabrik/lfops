source /tmp/lib.sh
source /tmp/lib-apache-httpd.sh

if [ $(httpd -M 2> /dev/null | grep ' reqtimeout_module' | wc -l) -eq 0 ]; then exit $FAIL; fi

if [ -z "$APACHE_CONF" ]; then
    echo "http://localhost/server-info not found or does not return any data"
    exit $FAIL
fi

conf=$(echo "$APACHE_CONF" | grep -i ";RequestReadTimeout " | grep -i "body=")

if [ -n "$conf" ]; then
    # directive was used and configured, Apache applied no default value, so:

    lines=$(extract "$conf" '<i>' '</i>')
    echo verify RequestReadTimeout directive
    echo -----------------------------------
    echo ''
    echo "$lines"
    echo ''
    exit $REV
fi

exit $FAIL
