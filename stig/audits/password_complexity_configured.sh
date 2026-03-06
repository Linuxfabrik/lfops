source /tmp/lib.sh

grep -Psi -- '^\h*(minclass|[dulo]credit)\b' \
  /etc/security/pwquality.conf /etc/security/pwquality.conf.d/*.conf >/dev/null 2>&1 || exit $FAIL

grep -Psi -- '^\h*password\h+(requisite|required|sufficient)\h+pam_pwquality\.so\h+([^#\n\r]+\h+)?(minclass=[0-3]|[dulo]credit=[^-]\d*)\b' \
  /etc/pam.d/system-auth /etc/pam.d/password-auth >/dev/null 2>&1 && exit $FAIL

exit $PASS