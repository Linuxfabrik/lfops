source /tmp/lib.sh

file=/etc/login.defs
days=7
if [ ! -e $file ]; then exit $FAIL; fi
if [ $(grep --count "^PASS_WARN_AGE" $file) -ne 1 ]; then exit $FAIL; fi
if [ $(awk '/^PASS_WARN_AGE/ {print $2}' $file) -lt $days ]; then exit $FAIL; fi
for i in $(grep -E ^[^:]+:[^\!*] /etc/shadow | cut -d: -f1); do
    if [ $(chage --list $i 2>/dev/null | awk '/warning/ {print $10}') -lt $days ]; then exit $FAIL; fi
done
exit $PASS
