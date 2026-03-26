source /tmp/lib.sh

l_valid_shells="^($(awk -F\/ '$NF != "nologin" {print}' /etc/shells | sed -rn '/^\//{s,/,\\\\/,g;p}' | paste -s -d '|' - ))$"

noncompliant="$(
while IFS= read -r l_user; do
    passwd -S "$l_user" 2>/dev/null | awk '$2 !~ /^L/ {print $1}'
done < <(awk -v pat="$l_valid_shells" -F: '($1 != "root" && $(NF) !~ pat) {print $1}' /etc/passwd)
)"

if [ -n "$noncompliant" ]; then
    exit $FAIL
fi

exit $PASS