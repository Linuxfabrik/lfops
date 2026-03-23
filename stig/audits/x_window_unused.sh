source /tmp/lib.sh

if is_not_installed 'xorg-x11-server-common'; then
  exit $PASS
fi
exit $FAIL
