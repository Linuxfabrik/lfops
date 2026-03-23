source /tmp/lib.sh

service_unused 'dnsmasq' dnsmasq.service && exit $PASS || exit $FAIL
