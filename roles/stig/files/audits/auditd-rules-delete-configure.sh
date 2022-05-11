source /tmp/lib.sh

search_term='key=delete'
expected='-a always,exit -F arch=b64 -S rename,unlink,unlinkat,renameat -F auid>=1000 -F auid!=-1 -F key=delete\n
    -a always,exit -F arch=b32 -S unlink,rename,unlinkat,renameat -F auid>=1000 -F auid!=-1 -F key=delete'
if diff <(echo -e $expected | sed 's/^\s*//') <(auditctl -l | grep $search_term) &>/dev/null; then exit $PASS; fi
exit $FAIL
