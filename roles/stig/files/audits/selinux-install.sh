source /tmp/lib.sh

if is_not_installed 'libselinux'; then exit $FAIL; fi
exit $PASS
