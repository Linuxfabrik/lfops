source /tmp/lib.sh

root_status="$(passwd -S root 2>/dev/null | awk '{print $2}')"

if [ "$root_status" = "P" ] || [ "$root_status" = "L" ]; then
    exit $PASS
fi

exit $FAIL