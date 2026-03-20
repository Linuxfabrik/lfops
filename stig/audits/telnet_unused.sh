source /tmp/lib.sh

service_unused 'telnet-server' telnet.socket && exit $PASS || exit $FAIL
