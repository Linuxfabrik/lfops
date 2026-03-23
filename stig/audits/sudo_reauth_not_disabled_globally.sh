source /tmp/lib.sh

if grep -rPq -- '^[^#].*!authenticate\b' /etc/sudoers* 2>/dev/null; then
  exit $FAIL
fi

exit $PASS