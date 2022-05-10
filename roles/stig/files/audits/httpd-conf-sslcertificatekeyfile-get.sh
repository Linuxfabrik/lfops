source /tmp/lib.sh
source /tmp/lib-apache-httpd.sh

if [ -z "$APACHE_CONF" ]; then
    echo "http://localhost/server-info not found or does not return any data"
    exit $FAIL
fi

audit_lines=""
conf=$(echo "$APACHE_CONF" | grep -i ";SSLCertificateKeyFile ")

if [ -n "$conf" ]; then
    # directive was used and configured, Apache applied no default value, so:

    lines=$(extract "$conf" '<i>' '</i>')
    while IFS= read -r line; do
        if ! test_perms 400 $line; then audit_lines="$audit_lines$line "; fi
    done <<< "$lines"
fi

if [ -n "$audit_lines" ]; then
    echo change ownership and permissions to 0400 of key files
    echo -----------------------------------------------------
    echo ''
    echo "$audit_lines"
    echo ''
    exit $FAIL
fi

exit $REV
