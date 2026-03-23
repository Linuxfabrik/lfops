source /tmp/lib.sh

if ! find / -xdev \( -path /proc -o -path /proc/\* -o -path /sys -o -path /sys/\* -o -path /run/user -o -path /run/user/\* \) -prune -o -type f -perm -0002 -print -quit 2>/dev/null | grep -q . && ! find / -xdev \( -path /proc -o -path /proc/\* -o -path /sys -o -path /sys/\* -o -path /run/user -o -path /run/user/\* \) -prune -o -type d -perm -0002 ! -perm -1000 -print -quit 2>/dev/null | grep -q .; then exit $PASS; fi
exit $FAIL
