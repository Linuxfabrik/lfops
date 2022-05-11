source /tmp/lib.sh
source /tmp/lib-apache-httpd.sh

if [ "$(grep $APACHE_USER /etc/passwd | cut -d':' -f7)" == "/sbin/nologin" ]; then exit $PASS; fi
if [ "$(grep $APACHE_USER /etc/passwd | cut -d':' -f7)" == "/usr/sbin/nologin" ]; then exit $PASS; fi
if [ "$(grep $APACHE_USER /etc/passwd | cut -d':' -f7)" == "/bin/false" ]; then exit $PASS; fi

exit $FAIL
