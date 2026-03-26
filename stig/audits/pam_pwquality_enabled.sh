source /tmp/lib.sh

for f in /etc/pam.d/system-auth /etc/pam.d/password-auth; do
  grep -Pq '\bpam_pwquality\.so\b' "$f" 2>/dev/null || exit $FAIL
done

exit $PASS
