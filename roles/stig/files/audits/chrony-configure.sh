source /tmp/lib.sh

if is_not_installed 'chrony'; then exit $SKIP; fi
if ! grep -E "^(server|pool) .*$" /etc/chrony.conf &>/dev/null; then exit $FAIL; fi
if [ -f /etc/sysconfig/chronyd ]; then
    if [ $( grep --count 'OPTIONS\s*=\s*.*-u chrony' /etc/sysconfig/chronyd ) -eq 0 ]; then exit $FAIL; fi
else
    exit $FAIL
fi
exit $PASS
