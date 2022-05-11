source /tmp/lib.sh

search_term='identity'
expected='-w /etc/group -p wa -k identity\n
    -w /etc/passwd -p wa -k identity\n
    -w /etc/gshadow -p wa -k identity\n
    -w /etc/shadow -p wa -k identity\n
    -w /etc/security/opasswd -p wa -k identity'
if diff <(echo -e $expected | sed 's/^\s*//') <(auditctl -l | grep $search_term) &>/dev/null; then exit $PASS; fi
exit $FAIL
