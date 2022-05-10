source /tmp/lib.sh

if is_installed 'samba'; then exit $FAIL; fi
exit $PASS
