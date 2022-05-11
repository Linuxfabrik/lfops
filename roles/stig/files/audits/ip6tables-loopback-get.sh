source /tmp/lib.sh

if ! ipv6_is_enabled; then exit $SKIP; fi
if is_active 'firewalld'; then exit $SKIP; fi
if is_active 'nftables'; then exit $SKIP; fi
if is_not_installed 'ip6tables'; then exit $SKIP; fi
str=$(iptables --list-rules --wait 60)
if [ $(echo "$str" | grep -E --count -- "-A INPUT -i lo( -m .*)? -j ACCEPT") == 0 ]; then exit $FAIL; fi
if [ $(echo "$str" | grep -E --count -- "-A OUTPUT -o lo( -m .*)? -j ACCEPT") == 0 ]; then exit $FAIL; fi
# this will rarely match in real-world firewalls
#if [ $(echo "$str" | grep -E --count -- "-A INPUT -s 127\.0\.0\.0\/8( -m .*)? -j (LOG_)?DROP") == 0 ]; then exit $FAIL; fi
exit $PASS
