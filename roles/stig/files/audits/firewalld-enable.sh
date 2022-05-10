source /tmp/lib.sh

if is_not_installed 'firewalld'; then exit $FAIL; fi
if is_disabled 'firewalld'; then exit $FAIL; fi
if [ "$(firewall-cmd --state 2> /dev/null)" != 'running' ]; then exit $FAIL; fi
exit $PASS
