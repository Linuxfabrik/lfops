source /tmp/lib.sh
source /tmp/lib-apache-httpd.sh

if [ $(httpd -M 2> /dev/null | grep 'auth_basic_module' | wc -l) -ne 0 ]; then exit $FAIL; fi
if [ $(httpd -M 2> /dev/null | grep 'auth_digest_module' | wc -l) -ne 0 ]; then exit $FAIL; fi
exit $PASS
