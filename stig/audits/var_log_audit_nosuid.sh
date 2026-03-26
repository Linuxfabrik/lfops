source /tmp/lib.sh

has_mount_option /var/log/audit nosuid && exit $PASS || exit $FAIL
