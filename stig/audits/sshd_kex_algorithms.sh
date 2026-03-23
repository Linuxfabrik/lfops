source /tmp/lib.sh

if [ -z "$(sshd -T | grep -Pi -- 'kexalgorithms\h+([^#\n\r]+,)?(diffie-hellman-group1-sha1|diffie-hellman-group14-sha1|diffie-hellman-group-exchange-sha1)\b')" ]; then exit $PASS; fi
exit $FAIL  
