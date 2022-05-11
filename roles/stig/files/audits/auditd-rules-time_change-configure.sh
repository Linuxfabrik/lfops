source /tmp/lib.sh

search_term='time-change'
expected='-a always,exit -F arch=b64 -S adjtimex,settimeofday -F key=time-change\n
    -a always,exit -F arch=b32 -S stime,settimeofday,adjtimex -F key=time-change\n
    -a always,exit -F arch=b64 -S clock_settime -F key=time-change\n
    -a always,exit -F arch=b32 -S clock_settime -F key=time-change\n
    -w /etc/localtime -p wa -k time-change'
if diff <(echo -e $expected | sed 's/^\s*//') <(auditctl -l | grep $search_term) &>/dev/null; then exit $PASS; fi
exit $FAIL
