source /tmp/lib.sh

files=(/etc/pam.d/password-auth /etc/pam.d/system-auth)

re='^\h*(auth|account|password|session)\h+(requisite|required|sufficient)\h+pam_unix\.so\b'

for f in "${files[@]}"; do
  [ -f "$f" ] || continue

  while IFS= read -r line; do
    if grep -Pq '\bnullok\b' <<<"$line"; then
      exit $FAIL
    fi
  done < <(grep -P -- "$re" "$f" 2>/dev/null)
done

exit $PASS