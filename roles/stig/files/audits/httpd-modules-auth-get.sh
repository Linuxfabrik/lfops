source /tmp/lib.sh
source /tmp/lib-apache-httpd.sh

audit_lines=$(httpd -M 2> /dev/null | grep -E 'auth._')
echo check which auth modules are loaded
echo -----------------------------------
echo ''
echo "$audit_lines"
echo ''
exit $REV
