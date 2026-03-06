source /tmp/lib.sh

if is_not_installed 'telnet'; then
  exit $PASS
fi
exit $FAIL