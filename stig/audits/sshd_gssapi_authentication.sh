source /tmp/lib.sh

if [ "$(sshd -T | awk '/^gssapiauthentication/{print $2}')" = "no" ]; then
  exit $PASS
fi

exit $FAIL
