source /tmp/lib.sh

if is_not_installed authselect; then exit $SKIP; fi
if [ "$(authselect current)" != 'No existing configuration detected.' ]; then exit $PASS; fi
exit $FAIL
