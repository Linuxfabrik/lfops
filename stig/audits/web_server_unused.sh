source /tmp/lib.sh

service_unused 'httpd' httpd.socket httpd.service || exit $FAIL
service_unused 'nginx' nginx.service || exit $FAIL
exit $PASS
