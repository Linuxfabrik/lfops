source /tmp/lib.sh
source /tmp/lib-apache-httpd.sh

if [ -z "$APACHE_CONF" ]; then
    echo "http://localhost/server-info not found or does not return any data"
    exit $FAIL
fi

conf=$(echo "$APACHE_CONF" | grep -i ";SSLUseStapling ")

if [ -n "$conf" ]; then
    # directive was used and configured, Apache applied no default value, so:

    lines=$(extract "$conf" '<i>' '</i>')
    while IFS= read -r line; do
        if [[ "$line" != *'on'* ]]; then exit $FAIL; fi
    done <<< "$lines"
fi

conf=$(echo "$APACHE_CONF" | grep -i ";SSLStaplingCache ")

if [ -n "$conf" ]; then
    # directive was used and configured, Apache applied no default value, so:

    lines=$(extract "$conf" '<i>' '</i>')
    while IFS= read -r line; do
        if [[ "$line" == *'dbm:'* ]]; then exit $PASS; fi
        if [[ "$line" == *'dc:unix:'* ]]; then exit $PASS; fi
        if [[ "$line" == *'shmcb:'* ]]; then exit $PASS; fi
    done <<< "$lines"
fi

exit $FAIL
