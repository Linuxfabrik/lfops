source /tmp/lib.sh

pass_warn="$(grep -Pi -- '^\h*PASS_WARN_AGE\h+\d+\b' /etc/login.defs | awk '{print $2}')"

if [ -z "$pass_warn" ] || [ "$pass_warn" -lt 7 ]; then
    exit $FAIL
fi

non_compliant_users="$(awk -F: '($2~/^\$.+\$/) { if ($6 < 7) print $1 }' /etc/shadow)"

if [ -n "$non_compliant_users" ]; then
    exit $FAIL
fi

exit $PASS