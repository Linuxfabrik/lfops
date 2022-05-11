source /tmp/lib.sh

if is_not_installed 'iptables'; then exit $FAIL; fi
if is_disabled 'iptables'; then exit $FAIL; fi
if is_enabled 'nftables'; then exit $FAIL; fi
if is_active 'nftables'; then exit $FAIL; fi
exit $PASS
