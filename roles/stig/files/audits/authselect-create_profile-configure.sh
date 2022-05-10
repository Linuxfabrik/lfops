source /tmp/lib.sh

if is_not_installed authselect; then exit $SKIP; fi
if [ -z $(authselect current | grep 'Profile ID: custom') ]; then exit $FAIL; fi
exit $PASS
