source /tmp/lib.sh

l_config_file="$(whereis aide.conf | awk '{print $2}')"
[ -f "$l_config_file" ] || exit $FAIL

l_systemd_analyze="$(whereis systemd-analyze | awk '{print $2}')"
a_audit_files=("auditctl" "auditd" "ausearch" "aureport" "autrace" "augenrules")
a_items=("p" "i" "n" "u" "g" "s" "b" "acl" "xattrs" "sha512")

fail=0
for l_audit_file in "${a_audit_files[@]}"; do
  [ -f "$(readlink -f "/sbin/$l_audit_file")" ] || continue
  l_match="$("$l_systemd_analyze" cat-config "$l_config_file" 2>/dev/null | grep -Po "^\h*(\/usr)?\/sbin\/$l_audit_file\b.*")"
  if [ -z "$l_match" ]; then
    fail=1; continue
  fi
  for l_var in "${a_items[@]}"; do
    grep -Pq "\b$l_var\b" <<< "$l_match" || { fail=1; break; }
  done
done

if [ "$fail" -eq 0 ]; then
  exit $PASS
else
  exit $FAIL
fi
