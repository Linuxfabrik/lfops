source /tmp/lib.sh

if is_not_installed 'nftables'; then exit $SKIP; fi
if is_disabled 'nftables'; then exit $SKIP; fi
if [ $(nft list ruleset | awk '/hook input/,/}/' | grep 'iif "lo" accept' | wc -l) -eq 0 ]; then exit $FAIL; fi
if [ $(nft list ruleset | awk '/hook input/,/}/' | grep 'ip sddr' | wc -l) -eq 0 ]; then exit $FAIL; fi
if [ $(nft list ruleset | awk '/hook input/,/}/' | grep 'ip6 saddr' | wc -l) -eq 0 ]; then exit $FAIL; fi
exit $PASS
