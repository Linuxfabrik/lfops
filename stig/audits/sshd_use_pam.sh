source /tmp/lib.sh

if [ "$(sshd -T | awk '/^usepam/{print $2}')" = "yes" ]; then
  exit $PASS
fi
exit $FAIL
