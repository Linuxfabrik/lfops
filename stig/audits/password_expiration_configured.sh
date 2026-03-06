source /tmp/lib.sh

pass_max_days="$(grep -Pi -- '^\h*PASS_MAX_DAYS\h+\d+\b' /etc/login.defs 2>/dev/null | awk '{print $2}' | tail -n 1)"
[ -n "$pass_max_days" ] || exit $FAIL
[ "$pass_max_days" -ge 1 ] 2>/dev/null || exit $FAIL
[ "$pass_max_days" -le 365 ] 2>/dev/null || exit $FAIL

awk -F: '($2~/^\$.+\$/) {if($5 > 365 || $5 < 1) exit 1}' /etc/shadow 2>/dev/null || exit $FAIL

exit $PASS