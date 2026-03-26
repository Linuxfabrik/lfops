source /tmp/lib.sh      

if [ -n "$(sshd -T | grep -Pi -- '(clientaliveinterval|clientalivecountmax)')" ]; then
  exit $PASS
fi
exit $FAIL
