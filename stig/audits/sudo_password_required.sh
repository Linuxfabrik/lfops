source /tmp/lib.sh

if grep -rPq -- '^[^#].*NOPASSWD' /etc/sudoers* 2>/dev/null; then
  exit $FAIL
fi

exit $PASS