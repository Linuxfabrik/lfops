source /tmp/lib.sh

if ! comm -23 <(awk -F: '{print $4}' /etc/passwd | sort -u) <(awk -F: '{print $3}' /etc/group | sort -u) | grep -q .; then exit $PASS; fi
exit $FAIL
