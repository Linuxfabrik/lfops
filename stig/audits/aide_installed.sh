source /tmp/lib.sh

if is_installed 'aide'; then
  exit $PASS
fi
exit $FAIL