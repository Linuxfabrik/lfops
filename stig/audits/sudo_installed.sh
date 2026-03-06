source /tmp/lib.sh

if is_installed 'sudo'; then
  exit $PASS
fi
exit $FAIL