source /tmp/lib.sh

pam_re='^\h*auth\h+(?:required|requisite)\h+pam_wheel\.so\h+(?:[^#\n\r]+\h+)?((?!\2)(use_uid\b|group=\H+\b))\h+(?:[^#\n\r]+\h+)?((?!\1)(use_uid\b|group=\H+\b))(\h+.*)?$'

# Must have the pam_wheel line (with use_uid and group=...)
line="$(grep -Pi -- "$pam_re" /etc/pam.d/su 2>/dev/null | head -n1)"
[ -n "$line" ] || exit $FAIL

#extract group name from group=<group_name>
grp="$(grep -oP 'group=\K\S+' <<< "$line" 2>/dev/null | head -n1)"
[ -n "$grp" ] || exit $FAIL

#group must exist and contain no users (4th field empty)
awk -F: -v g="$grp" '($1==g){ if($4=="") exit 0; else exit 1 } END{ exit 1 }' /etc/group 2>/dev/null || exit $FAIL

exit $PASS