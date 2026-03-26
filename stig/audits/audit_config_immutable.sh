source /tmp/lib.sh

grep -Ph -- '^\h*-e\h+2\b' /etc/audit/rules.d/*.rules | tail -1 | grep -q '.' || exit $FAIL

exit $PASS
