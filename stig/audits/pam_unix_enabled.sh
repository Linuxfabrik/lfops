source /tmp/lib.sh

# we expect pam_unix.so to appear at least in these stacks:
# - auth (typically sufficient)
# - account (typically required)
# - password (typically sufficient + sha512 shadow)
# - session (typically required)


re_auth='^\h*auth\h+\H+\h+pam_unix\.so\b'
re_acct='^\h*account\h+\H+\h+pam_unix\.so\b'
re_pass='^\h*password\h+\H+\h+pam_unix\.so\b.*\bsha512\b.*\bshadow\b'
re_sess='^\h*session\h+\H+\h+pam_unix\.so\b'

for f in /etc/pam.d/password-auth /etc/pam.d/system-auth; do
  grep -Pq -- "$re_auth" "$f" 2>/dev/null || exit $FAIL
  grep -Pq -- "$re_acct" "$f" 2>/dev/null || exit $FAIL
  grep -Pq -- "$re_pass" "$f" 2>/dev/null || exit $FAIL
  grep -Pq -- "$re_sess" "$f" 2>/dev/null || exit $FAIL
done

exit $PASS