source /tmp/lib.sh

if systemctl is-enabled firewalld.service 2>/dev/null | grep -q 'enabled'; then exit $PASS; fi
if ! systemctl is-enabled nftables.service 2>/dev/null | grep -q 'enabled'; then exit $FAIL; fi

if ! nft list ruleset 2>/dev/null | awk '/hook\s+input\s+/,/\}\s*(#.*)?$/' | grep -Pq -- '\H+\h+"lo"\h+accept'; then exit $FAIL; fi

l_ipsaddr="$(nft list ruleset 2>/dev/null | awk '/filter_IN_public_deny|hook\s+input\s+/,/\}\s*(#.*)?$/' | grep -P -- 'ip\h+saddr')"
if ! ( grep -Pq -- 'ip\h+saddr\h+127\.0\.0\.0\/8\h+(counter\h+packets\h+\d+\h+bytes\h+\d+\h+)?drop' <<< "$l_ipsaddr" || grep -Pq -- 'ip\h+daddr\h+\!\=\h+127\.0\.0\.1\h+ip\h+saddr\h+127\.0\.0\.1\h+drop' <<< "$l_ipsaddr" ); then exit $FAIL; fi

if grep -Pq -- '^\h*0\h*$' /sys/module/ipv6/parameters/disable; then
  l_ip6saddr="$(nft list ruleset 2>/dev/null | awk '/filter_IN_public_deny|hook input/,/}/' | grep 'ip6 saddr')"
  if ! ( grep -Pq 'ip6\h+saddr\h+::1\h+(counter\h+packets\h+\d+\h+bytes\h+\d+\h+)?drop' <<< "$l_ip6saddr" || grep -Pq -- 'ip6\h+daddr\h+\!=\h+::1\h+ip6\h+saddr\h+::1\h+drop' <<< "$l_ip6saddr" ); then exit $FAIL; fi
fi

exit $PASS