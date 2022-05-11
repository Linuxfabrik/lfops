source /tmp/lib.sh

if [ $(grep "^root:" /etc/passwd | cut -f4 -d:) ]; then exit $PASS; fi
exit $FAIL
