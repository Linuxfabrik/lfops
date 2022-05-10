source /tmp/lib.sh

if is_enabled 'ip6tables'; then exit $PASS; fi
exit $FAIL
