source /tmp/lib.sh

invalid_gid0_users="$(awk -F: '($1 !~ /^(sync|shutdown|halt|operator)$/ && $4=="0") {print $1}' /etc/passwd)"

if [ "$invalid_gid0_users" != "root" ]; then
    exit $FAIL
fi

exit $PASS
