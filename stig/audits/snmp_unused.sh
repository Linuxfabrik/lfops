source /tmp/lib.sh

service_unused 'net-snmp' snmpd.service && exit $PASS || exit $FAIL
