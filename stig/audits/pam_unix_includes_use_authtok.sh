source /tmp/lib.sh

grep -Pq -- '^\h*password\h+([^#\n\r]+)\h+pam_unix\.so\h+([^#\n\r]+\h+)?use_authtok\b' /etc/pam.d/password-auth 2>/dev/null || exit $FAIL
grep -Pq -- '^\h*password\h+([^#\n\r]+)\h+pam_unix\.so\h+([^#\n\r]+\h+)?use_authtok\b' /etc/pam.d/system-auth 2>/dev/null || exit $FAIL

exit $PASS