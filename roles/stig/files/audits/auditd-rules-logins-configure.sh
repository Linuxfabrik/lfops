source /tmp/lib.sh

# no need to check the config files, because it matters if the
# rules are active

rules=$(auditctl -l | grep -E '(session|logins)')

if [[ $rules != *"-w /var/run/utmp -p wa -k session"* ]]; then
    exit $FAIL
fi
if [[ $rules != *"-w /var/log/wtmp -p wa -k logins"* ]]; then
    exit $FAIL
fi
if [[ $rules != *"-w /var/log/btmp -p wa -k logins"* ]]; then
    exit $FAIL
fi
exit $PASS
