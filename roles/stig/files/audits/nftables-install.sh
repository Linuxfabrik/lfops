source /tmp/lib.sh

if is_not_installed 'nftables'; then exit $FAIL; fi
exit $PASS
