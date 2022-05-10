source /tmp/lib.sh
source /tmp/lib-apache-httpd.sh

if is_installed 'httpd'; then exit $FAIL; fi
exit $PASS
