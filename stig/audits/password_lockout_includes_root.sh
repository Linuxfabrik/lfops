source /tmp/lib.sh

conf="/etc/security/faillock.conf"

if ! grep -Pi -- '^\h*(even_deny_root|root_unlock_time\h*=\h*\d+)\b' "$conf" >/dev/null 2>&1; then
  exit $FAIL
fi

rut="$(grep -Pi -- '^\h*root_unlock_time\h*=\h*\d+\b' "$conf" 2>/dev/null | head -n1 | grep -oP '\d+')"
if [ -n "$rut" ]; then
  [ "$rut" -ge 60 ] || exit $FAIL
fi

grep -Pi -- '^\h*root_unlock_time\h*=\h*([1-9]|[1-5][0-9])\b' "$conf" >/dev/null 2>&1 && exit $FAIL

grep -Pi -- '^\h*auth\h+([^#\n\r]+\h+)pam_faillock\.so\h+([^#\n\r]+\h+)?root_unlock_time\h*=\h*([1-9]|[1-5][0-9])\b' \
  /etc/pam.d/system-auth /etc/pam.d/password-auth >/dev/null 2>&1 && exit $FAIL

exit $PASS