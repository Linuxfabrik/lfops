source /tmp/lib.sh

if is_not_installed 'ftp'; then
  exit $PASS
fi
exit $FAIL