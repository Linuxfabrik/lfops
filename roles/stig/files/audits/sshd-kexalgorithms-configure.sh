source /tmp/lib.sh

if [ -n "$(sshd -T | grep -i kexalgorithms | grep -i diffie-hellman-group-exchange-sha1)" ]; then exit $FAIL; fi
if [ -n "$(sshd -T | grep -i kexalgorithms | grep -i diffie-hellman-group1-sha1)" ]; then exit $FAIL; fi
if [ -n "$(sshd -T | grep -i kexalgorithms | grep -i diffie-hellman-group14-sha1)" ]; then exit $FAIL; fi
exit $PASS
