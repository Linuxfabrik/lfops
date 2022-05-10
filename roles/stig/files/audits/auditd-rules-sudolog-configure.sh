source /tmp/lib.sh

search_term='actions'
expected='-w /var/log/sudo.log -p wa -k actions'
if diff <(echo -e $expected | sed 's/^\s*//') <(auditctl -l | grep $search_term) &>/dev/null; then exit $PASS; fi
exit $FAIL
