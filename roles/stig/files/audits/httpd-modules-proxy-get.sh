source /tmp/lib.sh
source /tmp/lib-apache-httpd.sh

if [ $(httpd -M 2> /dev/null | grep 'proxy_' | wc -l) -eq 0 ]; then exit $PASS; fi
exit $FAIL
