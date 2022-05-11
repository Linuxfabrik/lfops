source /tmp/lib.sh
source /tmp/lib-apache-httpd.sh

if [ $(passwd -S $APACHE_USER | grep 'Password locked') -ne 0  ]; then exit $FAIL; fi
exit $PASS
