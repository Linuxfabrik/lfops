source /tmp/lib.sh

if is_not_installed 'tftp'; then
  exit $PASS
fi
exit $FAIL