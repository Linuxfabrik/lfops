source /tmp/lib.sh

now_epoch="$(date +%s)"

non_compliant_users="$(
while IFS= read -r l_user; do
    l_change="$(date -d "$(chage --list "$l_user" | grep '^Last password change' | cut -d: -f2 | grep -v 'never$')" +%s 2>/dev/null)"
    [ -n "$l_change" ] || continue
    if [ "$l_change" -gt "$now_epoch" ]; then
        echo "$l_user"
    fi
done < <(awk -F: '$2~/^\$.+\$/{print $1}' /etc/shadow)
)"

if [ -n "$non_compliant_users" ]; then
    exit $FAIL
fi

exit $PASS