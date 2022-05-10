source /tmp/lib.sh
source /tmp/lib-apache-httpd.sh

if [ -z "$APACHE_CONF" ]; then
    echo "http://localhost/server-info not found or does not return any data"
    exit $FAIL
fi

conf=$(echo "$APACHE_CONF" | grep -i ";Header " | grep -i "Content-Security-Policy")

if [ -n "$conf" ]; then
    # directive was used and configured, Apache applied no default value, so:

    lines=$(extract "$conf" '<i>' '</i>')
    echo verify Content-Security-Policy header
    echo -------------------------------------
    echo ''
    echo "$lines"
    echo ''
    exit $REV
fi


conf=$(echo "$APACHE_CONF" | grep -i ";Header " | grep -i ";X-Frame-Options ")

if [ -n "$conf" ]; then
    # directive was used and configured, Apache applied no default value, so:

    lines=$(extract "$conf" '<i>' '</i>')
    echo verify X-Frame-Options header
    echo -----------------------------
    echo ''
    echo "$lines"
    echo ''
    exit $REV
fi

exit $FAIL
