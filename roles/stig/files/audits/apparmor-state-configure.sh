source /tmp/lib.sh

if is_not_installed 'apparmor'; then exit $SKIP; fi
if [ "$(aa-status --enabled && echo Enabled)" != "Enabled" ]; then exit $FAIL; fi
exit $PASS
