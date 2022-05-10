source /tmp/lib.sh

if ! ipv6_is_enabled; then exit $SKIP; fi
if is_active 'firewalld'; then exit $SKIP; fi
if is_active 'nftables'; then exit $SKIP; fi
if is_not_installed 'ip6tables'; then exit $SKIP; fi
str=$(iptables --list-rules --wait 60)
if [ $(echo "$str" | grep --count -- "-P INPUT (DROP|REJECT)") == 0 ]; then exit $FAIL; fi
if [ $(echo "$str" | grep --count -- "-P FORWARD (DROP|REJECT)") == 0 ]; then exit $FAIL; fi
if [ $(echo "$str" | grep --count -- "-P OUTPUT (DROP|REJECT)") == 0 ]; then exit $FAIL; fi
exit $PASS
