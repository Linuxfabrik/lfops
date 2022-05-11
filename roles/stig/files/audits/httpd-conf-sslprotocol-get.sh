source /tmp/lib.sh
source /tmp/lib-apache-httpd.sh

if [ -z "$APACHE_CONF" ]; then
    echo "http://localhost/server-info not found or does not return any data"
    exit $FAIL
fi

conf=$(echo "$APACHE_CONF" | grep -i ";SSLProtocol ")
if [ -n "$conf" ]; then
    # directive was used and configured, Apache applied no default value, so:

    lines=$(extract "$conf" '<i>' '</i>')
    while IFS= read -r line; do
        if [ "$line" == '-all +tlsv1.2 +tlsv1.3' ]; then continue; fi
        if [ "$line" == '-all +tlsv1.2' ]; then continue; fi
        if [ "$line" == '-all +tlsv1.3' ]; then continue; fi
        if [ "$line" == 'tlsv1.2 tlsv1.3' ]; then continue; fi
        if [ "$line" == 'tlsv1.2' ]; then continue; fi
        if [ "$line" == 'tlsv1.3 tlsv1.2' ]; then continue; fi
        if [ "$line" == 'tlsv1.3' ]; then continue; fi
        exit $FAIL
    done <<< "$lines"
    exit $PASS
fi

# Default Value:
# SSLProtocol all
exit $FAIL
