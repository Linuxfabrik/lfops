source /tmp/lib.sh

service_unused 'rsync-daemon' rsyncd.socket rsyncd.service && exit $PASS || exit $FAIL
