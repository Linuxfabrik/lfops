source /tmp/lib.sh

if sshd -T | grep -Pi '^\h*ignoreRhosts\h+yes\b' >/dev/null; then
  exit $PASS
fi

exit $FAIL
