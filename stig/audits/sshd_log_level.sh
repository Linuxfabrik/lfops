source /tmp/lib.sh

if sshd -T | grep -Pi '^\h*loglevel\h+(VERBOSE|INFO)\b' >/dev/null; then
  exit $PASS
fi

exit $FAIL
