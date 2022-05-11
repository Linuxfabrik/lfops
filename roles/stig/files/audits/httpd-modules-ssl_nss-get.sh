source /tmp/lib.sh
source /tmp/lib-apache-httpd.sh

if [ $(httpd -M 2> /dev/null | grep -E ' ssl_module| nss_module' | wc -l) -ge 1 ]; then exit $PASS; fi
exit $FAIL
