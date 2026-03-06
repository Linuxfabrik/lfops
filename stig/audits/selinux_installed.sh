source /tmp/lib.sh

if is_installed 'libselinux'; then exit $PASS; fi
exit $FAIL
