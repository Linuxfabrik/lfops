source /tmp/lib.sh

grep -Pi -- '^\h*unlock_time\h*=\h*(0|9[0-9][0-9]|[1-9][0-9]{3,})\b' /etc/security/faillock.conf >/dev/null 2>&1 || exit $FAIL

grep -Pi -- '^\h*auth\h+(requisite|required|sufficient)\h+pam_faillock\.so\h+([^#\n\r]+\h+)?unlock_time\h*=\h*([1-9]|[1-9][0-9]|[1-8][0-9][0-9])\b' \
  /etc/pam.d/system-auth /etc/pam.d/password-auth >/dev/null 2>&1 && exit $FAIL

exit $PASS