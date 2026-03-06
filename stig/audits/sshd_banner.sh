source /tmp/lib.sh      

if [ "$(sshd -T | awk '/^banner/{print $2}')" != "none" ]; then
  exit $PASS
fi
exit $FAIL
