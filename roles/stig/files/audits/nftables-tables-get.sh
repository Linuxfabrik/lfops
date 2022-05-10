source /tmp/lib.sh

if is_not_installed 'nftables'; then exit $SKIP; fi
if is_disabled 'nftables'; then exit $SKIP; fi
if [ $(nft list tables | wc -l) -eq 0 ]; then exit $FAIL; fi
exit $PASS
