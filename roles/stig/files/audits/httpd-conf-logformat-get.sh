source /tmp/lib.sh
source /tmp/lib-apache-httpd.sh

if [ -z "$APACHE_CONF" ]; then
    echo "http://localhost/server-info not found or does not return any data"
    exit $FAIL
fi

found=0


conf=$(echo "$APACHE_CONF" | grep -i ";LogFormat ")

if [ -n "$conf" ]; then
    # directive was used and configured, Apache applied no default value, so:

    lines=$(extract "$conf" '<i>' '</i>')
    echo verify LogFormat directive
    echo --------------------------
    echo ''
    echo "$lines"
    echo ''
    echo ''
    found=$(($found + 1))
fi


conf=$(echo "$APACHE_CONF" | grep -i ";CustomLog ")

if [ -n "$conf" ]; then
    # directive was used and configured, Apache applied no default value, so:

    lines=$(extract "$conf" '<i>' '</i>')
    echo verify CustomLog directive
    echo --------------------------
    echo ''
    echo "$lines"
    echo ''
    found=$(($found + 1))
fi

if [ $found == 2 ]; then exit $REV; fi
exit $FAIL
