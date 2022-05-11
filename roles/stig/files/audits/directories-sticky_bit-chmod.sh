source /tmp/lib.sh

if [ -n "$(df --local -P | awk '{if (NR!=1) print $6}' | xargs -I '{}' find '{}' -xdev -type d \( -perm -0002 -a ! -perm -1000 \) 2>/dev/null)" ]; then exit $FAIL; fi
exit $PASS
