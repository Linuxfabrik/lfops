source /tmp/lib.sh

l_perm_mask="0022"
a_audit_tools=("/sbin/auditctl" "/sbin/aureport" "/sbin/ausearch" "/sbin/autrace" "/sbin/auditd" "/sbin/augenrules")

for l_audit_tool in "${a_audit_tools[@]}"; do
  [ -e "$l_audit_tool" ] || continue
  l_mode="$(stat -Lc '%#a' "$l_audit_tool")"
  if [ $(( "$l_mode" & "$l_perm_mask" )) -gt 0 ]; then
    exit $FAIL
  fi
done

exit $PASS
