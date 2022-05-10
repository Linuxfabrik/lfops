source /tmp/lib.sh

## Note: auditctl performs some translation on the rules entered as per the standard,
##  so what we end up testing for here is not what is specified in the standard, but
##  is correct when used in real-world situations.
search_term='system-locale'
expected='-a always,exit -F arch=b64 -S sethostname,setdomainname -F key=system-locale\n
    -a always,exit -F arch=b32 -S sethostname,setdomainname -F key=system-locale\n
    -w /etc/issue -p wa -k system-locale\n
    -w /etc/issue.net -p wa -k system-locale\n
    -w /etc/hosts -p wa -k system-locale\n
    -w /etc/sysconfig/network -p wa -k system-locale'
if diff <(echo -e $expected | sed 's/^\s*//') <(auditctl -l | grep $search_term) &>/dev/null; then exit $PASS; fi
exit $FAIL
