source /tmp/lib.sh

if is_installed 'dovecot'; then exit $FAIL; fi
exit $PASS
