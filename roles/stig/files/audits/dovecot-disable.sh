source /tmp/lib.sh

if is_enabled 'dovecot'; then exit $FAIL; fi
exit $PASS
