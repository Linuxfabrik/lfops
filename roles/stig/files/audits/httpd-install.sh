source /tmp/lib.sh
source /tmp/lib-apache-httpd.sh

if is_not_installed 'httpd'; then exit $FAIL; fi
if is_disabled 'httpd'; then exit $FAIL; fi
if [ $(yum list installed 'httpd' | wc -l) -eq 0 ]; then exit $FAIL; fi
exit $PASS
