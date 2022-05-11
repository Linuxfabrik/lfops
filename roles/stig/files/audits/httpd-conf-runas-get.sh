source /tmp/lib.sh
source /tmp/lib-apache-httpd.sh

if [ -z "$APACHE_CONF" ]; then
    echo "http://localhost/server-info not found or does not return any data"
    exit $FAIL
fi

conf=$(echo "$APACHE_CONF" | grep -i ";User ")

if [ -n "$conf" ]; then
    # directive was used and configured, Apache applied no default value, so:

    lines=$(extract "$conf" '<i>' '</i>')
    while IFS= read -r line; do
        if [[ $line != *"$APACHE_USER"* ]]; then exit $FAIL; fi
    done <<< "$lines"
fi


conf=$(echo "$APACHE_CONF" | grep -i ";Group ")

if [ -n "$conf" ]; then
    # directive was used and configured, Apache applied no default value, so:

    lines=$(extract "$conf" '<i>' '</i>')
    while IFS= read -r line; do
        if [[ $line != *"$APACHE_GROUP"* ]]; then exit $FAIL; fi
    done <<< "$lines"
fi


if [ "$(ps aux | grep httpd | grep -v '^root' | cut -d' ' -f1 | sort | uniq)" != "$APACHE_USER" ]; then exit $FAIL; fi


echo Apache uid must be less than the UID_MIN
echo ----------------------------------------
echo ''
echo "$(grep '^UID_MIN' /etc/login.defs)"
echo "$(id apache)"
echo ''
echo ''

echo httpd process user name should match the configuration file
echo -----------------------------------------------------------
echo ''
echo "$(ps aux | grep httpd | grep -v '^root')"
echo ''

exit $PASS
