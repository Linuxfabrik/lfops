source /tmp/lib.sh

if [ ! -s /etc/issue ]; then exit $FAIL; fi
if [ -n "$(grep -E -i "(\\\\v|\\\\r|\\\\m|\\\\s|$(grep '^ID=' /etc/os-release | cut -d= -f2 | sed -e 's/"//g'))" /etc/issue)" ]; then exit $FAIL; fi
exit $PASS
