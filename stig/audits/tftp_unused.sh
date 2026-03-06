source /tmp/lib.sh

service_unused 'tftp-server' tftp.socket tftp.service && exit $PASS || exit $FAIL
