source /tmp/lib.sh
source /tmp/lib-apache-httpd.sh

if [ -z "$APACHE_CONF" ]; then
    echo "http://localhost/server-info not found or does not return any data"
    exit $FAIL
fi

conf=$(echo "$APACHE_CONF" | grep -i ";AllowOverride ")
if [ -n "$conf" ]; then
    # directive was used and configured, Apache applied no default value, so:

    lines=$(extract "$conf" '<i>' '</i>')
    echo ensure AllowOverride is set to None
    echo -----------------------------------
    echo ''
    echo "$lines"
    echo ''
fi

conf=$(echo "$APACHE_CONF" | grep -i ";AllowOverrideList ")
if [ -n "$conf" ]; then
    # directive was used and configured, Apache applied no default value, so:

    lines=$(extract "$conf" '<i>' '</i>')
    echo ensure there are no AllowOverrideList directives present
    echo --------------------------------------------------------
    echo ''
    echo "$lines"
    echo ''
fi

exit $REV
