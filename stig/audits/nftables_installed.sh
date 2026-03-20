source /tmp/lib.sh

if is_installed 'nftables'; then
  exit $PASS
fi
exit $FAIL
