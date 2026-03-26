source /tmp/lib.sh

service_unused 'dovecot' dovecot.socket dovecot.service || exit $FAIL
service_unused 'cyrus-imapd' cyrus-imapd.service || exit $FAIL
exit $PASS
