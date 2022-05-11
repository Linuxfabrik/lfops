source /tmp/lib.sh

if is_not_installed 'nftables'; then exit $SKIP; fi
if is_disabled 'nftables'; then exit $SKIP; fi
if [ $(nft list ruleset | awk '/hook input/,/}/' | grep -E 'ip protocol (tcp|udp|icmp) ct state' | wc -l) -eq 0 ]; then exit $FAIL; fi
if [ $(nft list ruleset | awk '/hook output/,/}/' | grep -E 'ip protocol (tcp|udp|icmp) ct state' | wc -l) -eq 0 ]; then exit $FAIL; fi
exit $PASS
