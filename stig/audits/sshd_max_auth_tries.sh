source /tmp/lib.sh      

if [ "$(sshd -T | awk '/^maxauthtries/{print $2}')" -le 4 ]; then
  exit $PASS
fi
exit $FAIL
