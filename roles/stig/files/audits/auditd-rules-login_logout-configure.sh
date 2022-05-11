source /tmp/lib.sh

search_term='log -p wa -k logins'
expected='-w /var/log/faillog -p wa -k logins\n
    -w /var/log/lastlog -p wa -k logins'
if diff <(echo -e $expected | sed 's/^\s*//') <(auditctl -l | grep "$search_term") &>/dev/null; then exit $PASS; fi
exit $FAIL
