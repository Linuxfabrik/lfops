source /tmp/lib.sh
source /tmp/lib-apache-httpd.sh

if [ -z "$APACHE_CONF" ]; then
    echo "http://localhost/server-info not found or does not return any data"
    exit $FAIL
fi

conf=$(echo "$APACHE_CONF" | grep -i ";Allow ")
if [ -n "$conf" ]; then
    # directive was used and configured, Apache applied no default value, so:

    lines=$(extract "$conf" '<i>' '</i>')
    echo replace Allow directives by Require
    echo -----------------------------------
    echo ''
    echo "$lines"
    echo ''
    exit $REV
fi

conf=$(echo "$APACHE_CONF" | grep -i ";Deny ")
if [ -n "$conf" ]; then
    # directive was used and configured, Apache applied no default value, so:

    lines=$(extract "$conf" '<i>' '</i>')
    echo replace Deny directives by Require
    echo ----------------------------------
    echo ''
    echo "$lines"
    echo ''
    exit $REV
fi

exit $PASS
