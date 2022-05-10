source /tmp/lib.sh

if [ $(grep -E --count "^password\s+sufficient\s+pam_unix.so.*sha512" /etc/pam.d/system-auth) -ne 1 ]; then exit $FAIL; fi
if [ $(grep -E --count "^password\s+sufficient\s+pam_unix.so.*sha512" /etc/pam.d/password-auth) -ne 1 ]; then exit $FAIL; fi
exit $PASS
