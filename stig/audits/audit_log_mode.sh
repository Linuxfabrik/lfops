source /tmp/lib.sh

[ -e "/etc/audit/auditd.conf" ] || exit $FAIL

l_audit_log_directory="$(dirname "$(awk -F= '/^\s*log_file\s*/{print $2}' /etc/audit/auditd.conf | xargs)")"
[ -d "$l_audit_log_directory" ] || exit $FAIL

l_perm_mask="0177"
if find "$l_audit_log_directory" -maxdepth 1 -type f -perm /"$l_perm_mask" | grep -q '.'; then
  exit $FAIL
fi

exit $PASS
