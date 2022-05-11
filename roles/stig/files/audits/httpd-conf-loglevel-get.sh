source /tmp/lib.sh
source /tmp/lib-apache-httpd.sh

if [ -z "$APACHE_CONF" ]; then
    echo "http://localhost/server-info not found or does not return any data"
    exit $FAIL
fi

conf=$(echo "$APACHE_CONF" | grep -i ";LogLevel ")
if [ -n "$conf" ]; then
    # directive was used and configured, Apache applied no default value, so:

    lines=$(extract "$conf" '<i>' '</i>')
    echo ensure LogLevel is set to "notice core:info" or below
    echo -----------------------------------------------------
    echo ''
    echo "$lines"
    echo ''
    echo ''
fi

conf=$(echo "$APACHE_CONF" | grep -i ";ErrorLog ")
if [ -n "$conf" ]; then
    # directive was used and configured, Apache applied no default value, so:

    lines=$(extract "$conf" '<i>' '</i>')
    echo verify ErrorLog directive
    echo -------------------------
    echo ''
    echo "$lines"
    echo ''
fi

# The following is the default configuration:
# LogLevel warn
# ErrorLog "logs/error_log"
exit $REV
