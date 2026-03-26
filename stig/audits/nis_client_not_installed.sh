source /tmp/lib.sh

if is_not_installed 'ypbind'; then
  exit $PASS
fi
exit $FAIL