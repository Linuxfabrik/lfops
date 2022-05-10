source /tmp/lib.sh

if is_installed 'audit audit-libs'; then exit $PASS; fi
exit $FAIL
