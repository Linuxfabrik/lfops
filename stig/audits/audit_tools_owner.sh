source /tmp/lib.sh

if stat -Lc "%n %U" /sbin/auditctl /sbin/aureport /sbin/ausearch /sbin/autrace /sbin/auditd /sbin/augenrules 2>/dev/null | awk '$2 != "root" {print}' | grep -q '.'; then
  exit $FAIL
fi

exit $PASS
