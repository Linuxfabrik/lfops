source /tmp/lib.sh

l_valid_shells="^($(awk -F\/ '$NF != "nologin" {print}' /etc/shells | sed -rn '/^\//{s,/,\\\\/,g;p}' | paste -s -d '|' - ))$"
l_uid_min=$(awk '/^\s*UID_MIN/{print $2}' /etc/login.defs)

l_result="$(awk -v pat="$l_valid_shells" -F: '($1!~/^(root|halt|sync|shutdown|nfsnobody)$/ && ($3<'"$l_uid_min"' || $3 == 65534) && $(NF) ~ pat) {print $1}' /etc/passwd)"

if [ -n "$l_result" ]; then
  exit $FAIL
fi

exit $PASS
