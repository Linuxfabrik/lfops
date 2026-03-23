source /tmp/lib.sh

grep -P -- '^\h*password\h+([^#\n\r]+)\h+pam_pwhistory\.so\h+([^#\n\r]+\h+)?use_authtok\b' \
  /etc/pam.d/password-auth /etc/pam.d/system-auth >/dev/null 2>&1 || exit $FAIL

exit $PASS