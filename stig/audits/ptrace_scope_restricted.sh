source /tmp/lib.sh

l_output="" l_output2=""
a_parlist=("kernel.yama.ptrace_scope=1")
l_ufwscf="$([ -f /etc/default/ufw ] && awk -F= '/^\s*IPT_SYSCTL=/ {print $2}' /etc/default/ufw)"

kernel_parameter_chk()
{
l_krp="$(sysctl "$l_kpname" 2>/dev/null | awk -F= '{print $2}' | xargs)" # Check running configuration
if [ "$l_krp" != "$l_kpvalue" ]; then
  exit $FAIL
fi

unset A_out; declare -A A_out # Check durable setting (files)
while read -r l_out; do
if [ -n "$l_out" ]; then
if [[ $l_out =~ ^\s*# ]]; then
l_file="${l_out//# /}"
else
l_kpar="$(awk -F= '{print $1}' <<< "$l_out" | xargs)"
[ "$l_kpar" = "$l_kpname" ] && A_out+=(["$l_kpar"]="$l_file")
fi
fi
done < <(/usr/lib/systemd/systemd-sysctl --cat-config 2>/dev/null | grep -Po '^\h*([^#\n\r]+|#\h*\/[^#\n\r\h]+\.conf\b)')

if [ -n "$l_ufwscf" ] && [ -f "$l_ufwscf" ]; then # Account for systems with UFW (Not covered by systemd-sysctl --cat-config)
l_kpar="$(grep -Po "^\h*$l_kpname\b" "$l_ufwscf" 2>/dev/null | xargs)"
l_kpar="${l_kpar//\//.}"
[ "$l_kpar" = "$l_kpname" ] && A_out+=(["$l_kpar"]="$l_ufwscf")
fi

if (( ${#A_out[@]} > 0 )); then
while IFS="=" read -r l_fkpname l_fkpvalue; do
l_fkpname="${l_fkpname// /}"; l_fkpvalue="${l_fkpvalue// /}"
if [ "$l_fkpvalue" != "$l_kpvalue" ]; then
  exit $FAIL
fi
done < <(grep -Po -- "^\h*$l_kpname\h*=\h*\H+" "${A_out[@]}")
else
exit $FAIL
fi
}

while IFS="=" read -r l_kpname l_kpvalue; do
l_kpname="${l_kpname// /}"; l_kpvalue="${l_kpvalue// /}"
kernel_parameter_chk
done < <(printf '%s\n' "${a_parlist[@]}")

exit $PASS