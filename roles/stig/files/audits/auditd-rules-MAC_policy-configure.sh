source /tmp/lib.sh

search_term='MAC-policy'
expected='-w /etc/selinux -p wa -k MAC-policy\n
    -w /usr/share/selinux -p wa -k MAC-policy'
if diff <(echo -e $expected | sed 's/^\s*//') <(auditctl -l | grep $search_term) &>/dev/null; then exit $PASS; fi
exit $FAIL
