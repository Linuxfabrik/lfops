source /tmp/lib.sh

if [ -n "$(sshd -T | grep -i ciphers | grep -i 3des-cbc)" ]; then exit $FAIL; fi
if [ -n "$(sshd -T | grep -i ciphers | grep -i aes128-cbc)" ]; then exit $FAIL; fi
if [ -n "$(sshd -T | grep -i ciphers | grep -i aes192-cbc)" ]; then exit $FAIL; fi
if [ -n "$(sshd -T | grep -i ciphers | grep -i aes256-cbc)" ]; then exit $FAIL; fi
if [ -n "$(sshd -T | grep -i ciphers | grep -i arcfour)" ]; then exit $FAIL; fi
if [ -n "$(sshd -T | grep -i ciphers | grep -i arcfour128)" ]; then exit $FAIL; fi
if [ -n "$(sshd -T | grep -i ciphers | grep -i arcfour256)" ]; then exit $FAIL; fi
if [ -n "$(sshd -T | grep -i ciphers | grep -i blowfish-cbc)" ]; then exit $FAIL; fi
if [ -n "$(sshd -T | grep -i ciphers | grep -i cast128-cbc)" ]; then exit $FAIL; fi
if [ -n "$(sshd -T | grep -i ciphers | grep -i rijndael-cbc@lysator.liu.se)" ]; then exit $FAIL; fi
exit $PASS
