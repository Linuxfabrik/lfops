source /tmp/lib.sh

if is_enabled 'smb'; then exit $FAIL; fi
exit $PASS
