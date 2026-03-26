source /tmp/lib.sh

if ! find / -xdev \( -path /proc -o -path /proc/\* -o -path /sys -o -path /sys/\* -o -path /run/user -o -path /run/user/\* \) -prune -o \( -nouser -o -nogroup \) -print -quit 2>/dev/null | grep -q .; then exit $PASS; fi
exit $FAIL
