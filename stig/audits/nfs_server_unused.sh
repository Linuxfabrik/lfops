source /tmp/lib.sh

service_unused 'nfs-utils' nfs-server.service && exit $PASS || exit $FAIL
