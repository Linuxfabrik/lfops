source /tmp/lib.sh

if [ "$(grep SELINUX=enforcing /etc/selinux/config)" != "SELINUX=enforcing" ]; then exit $FAIL; fi
if [ "$(sestatus | awk '/Current mode/ {print $3}')" != "enforcing" ]; then exit $FAIL; fi
exit $PASS
