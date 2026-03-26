source /tmp/lib.sh

grep -Psi -- '^\h*maxsequence\h*=\h*[1-3]\b' \
  /etc/security/pwquality.conf /etc/security/pwquality.conf.d/*.conf >/dev/null 2>&1 || exit $FAIL

grep -Psi -- '^\h*password\h+(requisite|required|sufficient)\h+pam_pwquality\.so\h+([^#\n\r]+\h+)?maxsequence\h*=\h*(0|[4-9]|[1-9][0-9]+)\b' \
  /etc/pam.d/system-auth /etc/pam.d/password-auth >/dev/null 2>&1 && exit $FAIL

exit $PASS