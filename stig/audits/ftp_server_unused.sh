source /tmp/lib.sh

service_unused 'vsftpd' vsftpd.service && exit $PASS || exit $FAIL
