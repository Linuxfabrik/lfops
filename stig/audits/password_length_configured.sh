source /tmp/lib.sh

grep -Psi -- '^\h*minlen\h*=\h*(1[4-9]|[2-9][0-9]|[1-9][0-9]{2,})\b' \
  /etc/security/pwquality.conf /etc/security/pwquality.conf.d/*.conf >/dev/null 2>&1 || exit $FAIL

grep -Psi -- '^\h*password\h+(requisite|required|sufficient)\h+pam_pwquality\.so\h+([^#\n\r]+\h+)?minlen\h*=\h*([0-9]|1[0-3])\b' \
  /etc/pam.d/system-auth /etc/pam.d/password-auth >/dev/null 2>&1 && exit $FAIL

exit $PASS