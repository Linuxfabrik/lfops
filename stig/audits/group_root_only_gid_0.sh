source /tmp/lib.sh

invalid_gid0_groups="$(awk -F: '$3=="0"{print $1}' /etc/group | grep -v '^root$')"

if [ -n "$invalid_gid0_groups" ]; then
    exit $FAIL
fi

exit $PASS