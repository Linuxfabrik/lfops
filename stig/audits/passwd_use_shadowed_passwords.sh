source /tmp/lib.sh

if ! awk -F: '($2 != "x" ) { print "User: \"" $1 "\" is not set to shadowed passwords "}' /etc/passwd | grep -q .; then exit $PASS; fi
exit $FAIL
