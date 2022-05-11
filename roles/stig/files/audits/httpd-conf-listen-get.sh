source /tmp/lib.sh
source /tmp/lib-apache-httpd.sh

if [ -z "$APACHE_CONF" ]; then
    echo "http://localhost/server-info not found or does not return any data"
    exit $FAIL
fi

conf=$(echo "$APACHE_CONF" | grep -i ";SSLCertificateKeyFile ")

if [ -n "$conf" ]; then
    # directive was used and configured, Apache applied no default value, so:

    lines=$(extract "$conf" '<i>' '</i>')
    while IFS= read -r line; do
        if [[ $line == '80' ]]; then exit $FAIL; fi
        if [[ $line == '*:80' ]]; then exit $FAIL; fi
        if [[ $line == '0.0.0.0:80' ]]; then exit $FAIL; fi
        if [[ $line == '[::ffff:0.0.0.0]:80' ]]; then exit $FAIL; fi
        if [[ $line == '8080' ]]; then exit $FAIL; fi
        if [[ $line == '*:8080' ]]; then exit $FAIL; fi
        if [[ $line == '0.0.0.0:8080' ]]; then exit $FAIL; fi
        if [[ $line == '[::ffff:0.0.0.0]:8080' ]]; then exit $FAIL; fi
        if [[ $line == '443' ]]; then exit $FAIL; fi
        if [[ $line == '*:443' ]]; then exit $FAIL; fi
        if [[ $line == '0.0.0.0:443' ]]; then exit $FAIL; fi
        if [[ $line == '[::ffff:0.0.0.0]:443' ]]; then exit $FAIL; fi
        if [[ $line == '8443' ]]; then exit $FAIL; fi
        if [[ $line == '*:8443' ]]; then exit $FAIL; fi
        if [[ $line == '0.0.0.0:8443' ]]; then exit $FAIL; fi
        if [[ $line == '[::ffff:0.0.0.0]:8443' ]]; then exit $FAIL; fi
    done <<< "$lines"
fi

exit $PASS
