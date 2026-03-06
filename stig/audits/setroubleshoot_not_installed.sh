source /tmp/lib.sh

if is_not_installed 'setroubleshoot'; then
  exit $PASS
fi
exit $FAIL