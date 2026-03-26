source /tmp/lib.sh

l_output="" l_output2=""
a_parlist=("Storage=none")
l_systemd_config_file="/etc/systemd/coredump.conf" # Main systemd configuration file

config_file_parameter_chk()
{
unset A_out; declare -A A_out # Check config file(s) setting
while read -r l_out; do
if [ -n "$l_out" ]; then
if [[ $l_out =~ ^\s*# ]]; then
l_file="${l_out//# /}"
else
l_systemd_parameter="$(awk -F= '{print $1}' <<< "$l_out" | xargs)"
grep -Piq -- "^\h*$l_systemd_parameter_name\b" <<< "$l_systemd_parameter" && A_out+=(["$l_systemd_parameter"]="$l_file")
fi
fi
done < <(/usr/bin/systemd-analyze cat-config "$l_systemd_config_file" 2>/dev/null | grep -Pio '^\h*([^#\n\r]+|#\h*\/[^#\n\r\h]+\.conf\b)')

if (( ${#A_out[@]} > 0 )); then # Assess output from files and generate output
while IFS="=" read -r l_systemd_file_parameter_name l_systemd_file_parameter_value; do
l_systemd_file_parameter_name="${l_systemd_file_parameter_name// /}"
l_systemd_file_parameter_value="${l_systemd_file_parameter_value// /}"
if ! grep -Piq "^\h*$l_systemd_parameter_value\b" <<< "$l_systemd_file_parameter_value"; then
  exit $FAIL
fi
done < <(grep -Pio -- "^\h*$l_systemd_parameter_name\h*=\h*\H+" "${A_out[@]}")
else
exit $FAIL
fi
}

while IFS="=" read -r l_systemd_parameter_name l_systemd_parameter_value; do # Assess and check parameters
l_systemd_parameter_name="${l_systemd_parameter_name// /}"
l_systemd_parameter_value="${l_systemd_parameter_value// /}"
config_file_parameter_chk
done < <(printf '%s\n' "${a_parlist[@]}")

exit $PASS