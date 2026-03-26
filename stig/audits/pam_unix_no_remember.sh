source /tmp/lib.sh

files=(/etc/pam.d/password-auth /etc/pam.d/system-auth)

re='^\h*password\h+([^#\n\r]+\h+)?pam_unix\.so\b'

for f in "${files[@]}"; do
  [ -f "$f" ] || continue

  while IFS= read -r line; do
    if grep -Pq '\bremember=[0-9]+\b' <<<"$line"; then
      exit $FAIL
    fi
  done < <(grep -Pi -- "$re" "$f" 2>/dev/null)
done

exit $PASS