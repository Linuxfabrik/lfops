source /tmp/lib.sh

if grep -Eisq '^\s*Enable\s*=\s*true' /etc/gdm/custom.conf 2>/dev/null; then
  exit $FAIL
fi

exit $PASS