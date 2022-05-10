source /tmp/lib.sh

if [ -z $(grep -i '^/s*crypto_policy=' /etc/sysconfig/sshd) ]; then exit $PASS; fi
exit $FAIL
