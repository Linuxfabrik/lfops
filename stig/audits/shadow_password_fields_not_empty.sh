source /tmp/lib.sh

if ! awk -F: '($2 == "" ) { print $1 " does not have a password "}' /etc/shadow | grep -q .; then exit $PASS; fi
exit $FAIL
