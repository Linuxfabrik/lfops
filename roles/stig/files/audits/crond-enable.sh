source /tmp/lib.sh

if is_enabled 'crond'; then exit $PASS; fi
exit $FAIL
