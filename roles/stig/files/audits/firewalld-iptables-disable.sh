source /tmp/lib.sh

if is_not_installed 'firewalld'; then exit $FAIL; fi
if is_disabled 'firewalld'; then exit $FAIL; fi
if is_enabled 'iptables'; then exit $FAIL; fi
if is_active 'iptables'; then exit $FAIL; fi
exit $PASS
