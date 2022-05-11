source /tmp/lib.sh

if is_not_installed 'firewalld'; then exit $FAIL; fi
if is_disabled 'firewalld'; then exit $FAIL; fi
if is_enabled 'nftables'; then exit $FAIL; fi
if is_active 'nftables'; then exit $FAIL; fi
exit $PASS
