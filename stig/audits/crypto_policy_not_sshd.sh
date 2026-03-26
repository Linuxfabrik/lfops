source /tmp/lib.sh

grep -Pi '^\h*CRYPTO_POLICY\h*=' /etc/sysconfig/sshd >/dev/null 2>&1 && exit $FAIL
exit $PASS