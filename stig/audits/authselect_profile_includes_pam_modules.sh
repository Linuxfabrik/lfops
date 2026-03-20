source /tmp/lib.sh

l_profile="$(head -1 /etc/authselect/authselect.conf 2>/dev/null)"
if [ -z "$l_profile" ]; then
  exit $FAIL
fi

l_base="/etc/authselect/$l_profile"
if [ ! -r "$l_base/system-auth" ] || [ ! -r "$l_base/password-auth" ]; then
  exit $FAIL
fi

if grep -Pq -- '\bpam_pwquality\.so\b' "$l_base"/{system,password}-auth 2>/dev/null \
  && grep -Pq -- '\bpam_pwhistory\.so\b' "$l_base"/{system,password}-auth 2>/dev/null \
  && grep -Pq -- '\bpam_faillock\.so\b' "$l_base"/{system,password}-auth 2>/dev/null \
  && grep -Pq -- '\bpam_unix\.so\b' "$l_base"/{system,password}-auth 2>/dev/null; then
  exit $PASS
else
  exit $FAIL
fi
