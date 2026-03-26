source /tmp/lib.sh

inactive_default="$(useradd -D | grep -E '^INACTIVE=' | awk -F= '{print $2}')"

if [ -z "$inactive_default" ] || [ "$inactive_default" -gt 45 ] || [ "$inactive_default" -lt 0 ]; then
    exit $FAIL
fi

non_compliant_users="$(awk -F: '($2~/^\$.+\$/) { if ($7 > 45 || $7 < 0) print $1 }' /etc/shadow)"

if [ -n "$non_compliant_users" ]; then
    exit $FAIL
fi

exit $PASS