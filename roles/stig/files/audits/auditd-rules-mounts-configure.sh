source /tmp/lib.sh

search_term='mounts'
expected='-a always,exit -F arch=b64 -S mount -F auid>=1000 -F auid!=-1 -F key=mounts\n
    -a always,exit -F arch=b32 -S mount -F auid>=1000 -F auid!=-1 -F key=mounts'
if diff <(echo -e $expected | sed 's/^\s*//') <(auditctl -l | grep $search_term) &>/dev/null; then exit $PASS; fi
exit $FAIL
