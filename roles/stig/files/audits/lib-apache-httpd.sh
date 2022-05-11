# list of result codes
PASS=0
FAIL=1
SKIP=2                      # not applicable
TODO=4                      # needs to be implemented
REV=8                       # review manually


if [ ! command -v curl &> /dev/null ]; then
    echo "curl not found"
    exit $FAIL
fi


# APACHE_CONF: we have to limit the output to a maximum number of lines, otherwise we can't grep or
# awk anymore later on in this shell script and get "Argument list too long". This often happens if
# the OWASP Rules Set is loaded.
if [ -e $APACHE_CONF ]; then
    if [ -d /etc/httpd ]; then
        export APACHE_PREFIX=/etc/httpd
        export APACHE_CONF=$(curl --silent --connect-timeout 1 --location --insecure http://localhost/server-info?config | head -n 550)
        export APACHE_USER=apache
        export APACHE_GROUP=apache
        export APACHE_DOCUMENT_ROOT=$(echo "$APACHE_CONF" | grep ';DocumentRoot ' | awk -F '&quot;' '{ print $2 }')
    fi

    if [ -d /etc/apache2 ]; then
        export APACHE_PREFIX=/etc/apache2
        export APACHE_CONF=$(curl --silent --connect-timeout 1 --location --insecure http://localhost/server-info?config | head -n 550)
        export APACHE_USER=www-data
        export APACHE_GROUP=www-data
        export APACHE_DOCUMENT_ROOT=$(echo "$APACHE_CONF" | grep ';DocumentRoot ' | awk -F '&quot;' '{ print $2 }')
    fi
    if [[ "$APACHE_CONF" == *"403 Forbidden"* ]]; then
        echo "http://localhost/server-info?config: 403 Forbidden"
        exit $FAIL
    fi
    if [[ "$APACHE_CONF" == *"404 Not Found"* ]]; then
        echo "http://localhost/server-info?config: 404 Not Found"
        exit $FAIL
    fi
    if [ -z "$APACHE_CONF" ]; then
        echo "http://localhost/server-info not found or does not return any data"
        exit $FAIL
    fi

fi
