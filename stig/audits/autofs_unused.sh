source /tmp/lib.sh

service_unused 'autofs' autofs.service && exit $PASS || exit $FAIL
