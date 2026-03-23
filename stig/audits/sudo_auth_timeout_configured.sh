source /tmp/lib.sh

if grep -roP 'timestamp_timeout=\K[0-9]+' /etc/sudoers* 2>/dev/null | awk '$1 > 15 { exit 1 }'; then
  exit $PASS
else
  exit $FAIL
fi