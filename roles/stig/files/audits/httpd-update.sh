source /tmp/lib.sh
source /tmp/lib-apache-httpd.sh

if [ $(yum check-update httpd &>/dev/null; echo $?) -eq 0 ]; then exit $PASS; fi
exit $REV
