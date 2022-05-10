source /tmp/lib.sh

search_term='modules'
expected='-w /sbin/insmod -p x -k modules\n
    -w /sbin/rmmod -p x -k modules\n
    -w /sbin/modprobe -p x -k modules\n
    -a always,exit -F arch=b32 -S init_module,delete_module -F key=modules\n
    -a always,exit -F arch=b64 -S init_module,delete_module -F key=modules'
if diff <(echo -e $expected | sed 's/^\s*//') <(auditctl -l | grep $search_term) &>/dev/null; then exit $PASS; fi
exit $FAIL
