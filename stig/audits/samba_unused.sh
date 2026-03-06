source /tmp/lib.sh

service_unused 'samba' smb.service && exit $PASS || exit $FAIL
