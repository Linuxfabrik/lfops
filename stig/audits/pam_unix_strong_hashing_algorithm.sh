source /tmp/lib.sh

files=(/etc/pam.d/password-auth /etc/pam.d/system-auth)

re='^\h*password\h+([^#\n\r]+)\h+pam_unix\.so\h+([^#\n\r]+\h+)?(sha512|yescrypt)\b'

for f in "${files[@]}"; do
  [ -f "$f" ] || exit $FAIL
  grep -Pq -- "$re" "$f" 2>/dev/null || exit $FAIL
done

exit $PASS