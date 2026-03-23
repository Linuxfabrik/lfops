source /tmp/lib.sh

[ -e "/etc/audit/auditd.conf" ] || exit $FAIL

l_audit_log_directory="$(dirname "$(awk -F= '/^\s*log_file\s*/{print $2}' /etc/audit/auditd.conf | xargs)")"
l_audit_log_group="$(awk -F= '/^\s*log_group\s*/{print $2}' /etc/audit/auditd.conf | xargs)"

grep -Pq -- '^\h*(root|adm)\h*$' <<< "$l_audit_log_group" || exit $FAIL
[ -d "$l_audit_log_directory" ] || exit $FAIL

if find "$l_audit_log_directory" -maxdepth 1 -type f \( ! -group root -a ! -group adm \) | grep -q '.'; then
  exit $FAIL
fi

exit $PASS
