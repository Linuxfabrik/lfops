source /tmp/lib.sh

if ! cut -f3 -d: /etc/group | sort -n | uniq -c | awk '($1 > 1) {print}' | grep -q .; then exit $PASS; fi
exit $FAIL
