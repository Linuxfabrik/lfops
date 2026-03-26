source /tmp/lib.sh

if ! cut -d: -f3 /etc/group | sort -n | uniq -d | grep -q .; then exit $PASS; fi
exit $FAIL
