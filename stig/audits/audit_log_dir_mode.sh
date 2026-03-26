source /tmp/lib.sh

[ -e "/etc/audit/auditd.conf" ] || exit $FAIL

l_audit_log_directory="$(dirname "$(awk -F= '/^\s*log_file\s*/{print $2}' /etc/audit/auditd.conf | xargs)")"
[ -d "$l_audit_log_directory" ] || exit $FAIL

l_perm_mask="0027"
l_directory_mode="$(stat -Lc '%#a' "$l_audit_log_directory")"
if [ $(( $l_directory_mode & $l_perm_mask )) -gt 0 ]; then
  exit $FAIL
fi

exit $PASS
