source /tmp/lib.sh

if is_not_installed 'chrony'; then exit $FAIL; fi
