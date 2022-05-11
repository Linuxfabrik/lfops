source /tmp/lib.sh

if ! ipv6_is_enabled; then exit $SKIP; fi
if is_active 'firewalld'; then exit $SKIP; fi
if is_active 'nftables'; then exit $SKIP; fi
if is_not_installed 'ip6tables'; then exit $SKIP; fi
str=$(iptables --list-rules --wait 60)
if [ $(echo "$str" | grep -E --count -- "-A INPUT -m state --state (RELATED,)?ESTABLISHED( -m .*)? -j ACCEPT") == 0 ]; then exit $FAIL; fi
if [ $(echo "$str" | grep -E --count -- "-A OUTPUT -m state --state RELATED,ESTABLISHED( -m .*)? -j ACCEPT") == 0 ]; then exit $FAIL; fi
exit $PASS
