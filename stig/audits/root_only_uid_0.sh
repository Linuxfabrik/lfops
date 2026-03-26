source /tmp/lib.sh

non_root_uid0="$(awk -F: '($3 == 0 && $1 != "root") { print $1 }' /etc/passwd)"

if [ -n "$non_root_uid0" ]; then
    exit $FAIL
fi

exit $PASS