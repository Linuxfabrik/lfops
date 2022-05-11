source /tmp/lib.sh

file=/etc/login.defs
days=365

if [ ! -e $file ]; then exit $FAIL; fi
if [ $(grep --count "^PASS_MAX_DAYS" $file) -ne 1 ]; then exit $FAIL; fi
if [ $(awk '/^PASS_MAX_DAYS/ {print $2}' $file) -gt $days ]; then exit $FAIL; fi
for i in $(grep -E ^[^:]+:[^\!*] /etc/shadow | cut -d: -f1); do
    if [ $(chage --list $i 2>/dev/null | awk '/Maximum/ {print $9}') -lt $days ]; then exit $FAIL; fi
done
exit $PASS
