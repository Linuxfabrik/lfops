source /tmp/lib.sh

if [ "$(getenforce)" == 'Disabled' ]; then exit $SKIP; fi
if [ "$(ps -eZ | grep httpd | cut -d':' -f3 | uniq)" == "httpd_t" ]; then exit $PASS; fi
if [ "$(ps -eZ | grep apache2 | cut -d':' -f3 | uniq)" == "httpd_t" ]; then exit $PASS; fi

exit $FAIL
