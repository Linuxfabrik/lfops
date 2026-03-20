source /tmp/lib.sh      

if [ "$(sshd -T | awk '/^maxsessions/{print $2}')" -le 10 ]; then
  exit $PASS
fi
exit $FAIL
