source /tmp/lib.sh

if is_installed 'chrony'; then exit $SKIP; fi
if is_not_installed 'ntp'; then exit $FAIL; fi
if ! grep -E "^(server|pool) .*$" /etc/ntp.conf &>/dev/null; then exit $FAIL; fi
if [ -f /etc/sysconfig/ntpd ]; then
    if [ $( grep --count 'OPTIONS\s*=\s*.*-u ntp:ntp' /etc/sysconfig/ntpd ) -eq 0 ]; then exit $FAIL; fi
else
    exit $FAIL
fi
exit $PASS
