source /tmp/lib.sh

inactive_days=$(useradd --defaults | grep INACTIVE | sed 's/^.*=//')
if [ -z "$inactive_days" ]; then exit $FAIL; fi

max_days=30
if [ $inactive_days -gt $max_days ]; then exit $FAIL; fi
if [ $inactive_days -eq -1 ]; then exit $FAIL; fi

for days in $(grep -E ^[^:]+:[^\!*] /etc/shadow | cut -d: -f7); do
    if [ $days -gt 30  ]; then exit $FAIL; fi
done

exit $PASS
