source /tmp/lib.sh

if [ ! -e /etc/motd ]; then exit $PASS; fi
if [ -n "$(grep -E -i "(\\\\v|\\\\r|\\\\m|\\\\s|$(grep '^ID=' /etc/os-release | cut -d= -f2 | sed -e 's/"//g'))" /etc/motd)" ]; then exit $FAIL; fi
exit $PASS
