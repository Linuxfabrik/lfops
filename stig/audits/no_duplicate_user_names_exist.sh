source /tmp/lib.sh

if ! cut -f1 -d: /etc/passwd | sort | uniq -d | grep -q .; then exit $PASS; fi
exit $FAIL
