source /tmp/lib.sh

service_unused 'avahi' avahi-daemon.socket avahi-daemon.service && exit $PASS || exit $FAIL
