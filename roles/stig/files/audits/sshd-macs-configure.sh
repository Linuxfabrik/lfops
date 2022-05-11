source /tmp/lib.sh

if [ -n "$(sshd -T | grep -i macs | grep -i hmac-md5)" ]; then exit $FAIL; fi
if [ -n "$(sshd -T | grep -i macs | grep -i hmac-md5-96)" ]; then exit $FAIL; fi
if [ -n "$(sshd -T | grep -i macs | grep -i hmac-md5-96-etm@openssh.com)" ]; then exit $FAIL; fi
if [ -n "$(sshd -T | grep -i macs | grep -i hmac-md5-etm@openssh.com)" ]; then exit $FAIL; fi
if [ -n "$(sshd -T | grep -i macs | grep -i hmac-ripemd160)" ]; then exit $FAIL; fi
if [ -n "$(sshd -T | grep -i macs | grep -i hmac-ripemd160-etm@openssh.com)" ]; then exit $FAIL; fi
if [ -n "$(sshd -T | grep -i macs | grep -i hmac-sha1)" ]; then exit $FAIL; fi
if [ -n "$(sshd -T | grep -i macs | grep -i hmac-sha1-96)" ]; then exit $FAIL; fi
if [ -n "$(sshd -T | grep -i macs | grep -i hmac-sha1-96-etm@openssh.com)" ]; then exit $FAIL; fi
if [ -n "$(sshd -T | grep -i macs | grep -i hmac-sha1-etm@openssh.com)" ]; then exit $FAIL; fi
if [ -n "$(sshd -T | grep -i macs | grep -i umac-128-etm@openssh.com)" ]; then exit $FAIL; fi
if [ -n "$(sshd -T | grep -i macs | grep -i umac-128@openssh.com)" ]; then exit $FAIL; fi
if [ -n "$(sshd -T | grep -i macs | grep -i umac-64-etm@openssh.com)" ]; then exit $FAIL; fi
if [ -n "$(sshd -T | grep -i macs | grep -i umac-64@openssh.com)" ]; then exit $FAIL; fi
exit $PASS
