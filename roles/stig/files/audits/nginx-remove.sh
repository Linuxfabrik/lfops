source /tmp/lib.sh

if is_installed 'nginx'; then exit $FAIL; fi
exit $PASS
