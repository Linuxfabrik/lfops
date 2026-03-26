source /tmp/lib.sh

pass_min_days="$(grep -Pi -- '^\h*PASS_MIN_DAYS\h+\d+\b' /etc/login.defs 2>/dev/null | awk '{print $2}' | tail -n 1)"
[ -n "$pass_min_days" ] || exit $FAIL
[ "$pass_min_days" -ge 1 ] 2>/dev/null || exit $FAIL

awk -F: '($2~/^\$.+\$/) {if($4 < 1) exit 1}' /etc/shadow 2>/dev/null || exit $FAIL

exit $PASS