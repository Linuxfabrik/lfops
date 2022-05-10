source /tmp/lib.sh

if is_installed 'firewalld'; then exit $PASS; fi
if is_installed 'iptables'; then exit $PASS; fi
if is_installed 'nftables'; then exit $PASS; fi
exit $FAIL
