source /tmp/lib.sh

if [ "$(grep -E "^\s*\*\s+hard\s+core" /etc/security/limits.conf /etc/security/limits.d/* 2> /dev/null | sed -e 's/^.*://' -e 's/\s//g' | sort | uniq)" != '*hardcore0' ]; then exit $FAIL; fi
if [ "$(sysctl fs.suid_dumpable 2> /dev/null)" != 'fs.suid_dumpable = 0' ]; then exit $FAIL; fi
# if [ "$(grep "^fs\.suid_dumpable" /etc/sysctl.conf /etc/sysctl.d/*  | sed -e 's/^.*://' -e 's/\s//g' | sort | uniq)" != 'fs.suid_dumpable=0' ]; then exit $FAIL; fi
exit $PASS
