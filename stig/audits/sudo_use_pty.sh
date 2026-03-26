source /tmp/lib.sh

grep -rPiq -- '^\h*Defaults\h+([^#\n\r]+,\h*)?use_pty\b' /etc/sudoers* 2>/dev/null || exit $FAIL

if grep -rPiq -- '^\h*Defaults\h+([^#\n\r]+,\h*)?!use_pty\b' /etc/sudoers* 2>/dev/null; then
  exit $FAIL
fi

exit $PASS