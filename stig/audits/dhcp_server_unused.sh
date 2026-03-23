source /tmp/lib.sh

service_unused 'dhcp-server' dhcpd.service dhcpd6.service && exit $PASS || exit $FAIL
