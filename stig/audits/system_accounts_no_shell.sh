source /tmp/lib.sh

l_valid_shells="^($(awk -F\/ '$NF != "nologin" {print}' /etc/shells | sed -rn '/^\//{s,/,\\\\/,g;p}' | paste -s -d '|' - ))$"

uid_min="$(awk '/^\s*UID_MIN/{print $2}' /etc/login.defs)"

bad_service_accounts="$(awk -v pat="$l_valid_shells" -v uidmin="$uid_min" -F: '($1!~/^(root|halt|sync|shutdown|nfsnobody)$/ && ($3<uidmin || $3 == 65534) && $(NF) ~ pat) {print $1}' /etc/passwd)"

if [ -n "$bad_service_accounts" ]; then
    exit $FAIL
fi

exit $PASS