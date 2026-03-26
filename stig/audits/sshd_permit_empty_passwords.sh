source /tmp/lib.sh      

if [ "$(sshd -T | awk '/^permitemptypasswords/{print $2}')" = "no" ]; then
  exit $PASS
fi
exit $FAIL
