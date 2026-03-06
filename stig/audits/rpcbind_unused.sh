source /tmp/lib.sh

service_unused 'rpcbind' rpcbind.socket rpcbind.service && exit $PASS || exit $FAIL
