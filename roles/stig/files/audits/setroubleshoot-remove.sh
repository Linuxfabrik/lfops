source /tmp/lib.sh

if is_installed 'setroubleshoot'; then exit $FAIL; fi
exit $PASS
