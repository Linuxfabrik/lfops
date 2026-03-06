source /tmp/lib.sh

re='^\h*password\h+required\h+pam_pwhistory\.so\b([^#\n\r]+\h+)?use_authtok\b'

for f in /etc/pam.d/password-auth /etc/pam.d/system-auth; do
  grep -Pq -- "$re" "$f" 2>/dev/null || exit $FAIL
done

exit $PASS