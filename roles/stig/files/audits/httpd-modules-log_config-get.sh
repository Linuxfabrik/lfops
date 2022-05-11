source /tmp/lib.sh
source /tmp/lib-apache-httpd.sh

if [ $(httpd -M 2> /dev/null | grep log_config | wc -l) -eq 0 ]; then exit $FAIL; fi
exit $PASS
