source /tmp/lib.sh

if [ ! -e /etc/motd ]; then exit $SKIP; fi
if test_perms 644 '/etc/motd'; then exit $PASS; fi
exit $FAIL
