source /tmp/lib.sh

grep -Pi -- '^\h*mac\h*=\h*([^#\n\r]+)?-64\b' /etc/crypto-policies/state/CURRENT.pol \
  >/dev/null 2>&1 && exit $FAIL
exit $PASS