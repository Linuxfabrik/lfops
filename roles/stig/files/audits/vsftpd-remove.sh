source /tmp/lib.sh

if is_installed 'vsftpd'; then exit $FAIL; fi
exit $PASS
