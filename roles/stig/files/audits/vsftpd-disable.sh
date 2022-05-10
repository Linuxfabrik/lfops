source /tmp/lib.sh

if is_enabled 'vsftpd'; then exit $FAIL; fi
exit $PASS
