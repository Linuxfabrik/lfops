source /tmp/lib.sh

if is_not_installed 'mcstrans'; then
  exit $PASS
fi
exit $FAIL