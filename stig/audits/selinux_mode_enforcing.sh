source /tmp/lib.sh

if grep -Eq '^\s*SELINUX=enforcing\b' /etc/selinux/config && \
   [ "$(getenforce)" = "Enforcing" ]; then
  exit $PASS
fi
exit $FAIL
