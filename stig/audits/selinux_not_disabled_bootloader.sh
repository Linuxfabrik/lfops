source /tmp/lib.sh      

if ! grubby --info=ALL | grep -Pq '(selinux|enforcing)=0\b'; then exit $PASS; fi
exit $FAIL
