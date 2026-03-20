source /tmp/lib.sh

grep -Pi -- '^\h*remember\h*=\h*(2[4-9]|[3-9][0-9]|[1-9][0-9]{2,})\b' \
  /etc/security/pwhistory.conf >/dev/null 2>&1 || exit $FAIL

grep -Pi -- '^\h*password\h+(requisite|required|sufficient)\h+pam_pwhistory\.so\h+([^#\n\r]+\h+)?remember=(2[0-3]|1[0-9]|[0-9])\b' \
  /etc/pam.d/system-auth /etc/pam.d/password-auth >/dev/null 2>&1 && exit $FAIL

exit $PASS