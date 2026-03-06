source /tmp/lib.sh      

if is_installed 'chrony'; then exit $PASS; fi
exit $FAIL