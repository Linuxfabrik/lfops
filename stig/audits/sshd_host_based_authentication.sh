source /tmp/lib.sh

if sshd -T | grep -Pi '^\h*hostbasedauthentication\h+no\b' >/dev/null; then
  exit $PASS
fi

exit $FAIL
