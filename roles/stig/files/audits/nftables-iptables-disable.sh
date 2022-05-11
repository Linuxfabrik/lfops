source /tmp/lib.sh

if is_not_installed 'nftables'; then exit $SKIP; fi
if is_disabled 'nftables'; then exit $SKIP; fi
if [ -n "$(iptables --list)" ]; then exit $FAIL; fi
if [ -n "$(ip6tables --list)" ]; then exit $FAIL; fi
exit $PASS
