source /tmp/lib.sh

any_pkg_installed "gdm gdm3" || exit $PASS

l_output2=""

# Look for existing settings and set variables if they exist
l_kfile="$(grep -Prils -- '^\h*automount\b' /etc/dconf/db/*.d 2>/dev/null | head -n1)"
l_kfile2="$(grep -Prils -- '^\h*automount-open\b' /etc/dconf/db/*.d 2>/dev/null | head -n1)"

# Set profile name based on dconf db directory ({PROFILE_NAME}.d)
l_gpname=""
if [ -n "$l_kfile" ] && [ -f "$l_kfile" ]; then
  l_gpname="$(awk -F\/ '{split($(NF-1),a,".");print a[1]}' <<< "$l_kfile")"
elif [ -n "$l_kfile2" ] && [ -f "$l_kfile2" ]; then
  l_gpname="$(awk -F\/ '{split($(NF-1),a,".");print a[1]}' <<< "$l_kfile2")"
fi

if [ -n "$l_gpname" ]; then
  l_gpdir="/etc/dconf/db/$l_gpname.d"

  grep -Pq -- "^\h*system-db:$l_gpname\b" /etc/dconf/profile/* 2>/dev/null || l_output2="$l_output2\n - dconf database profile isn't set"
  [ -f "/etc/dconf/db/$l_gpname" ] || l_output2="$l_output2\n - The dconf database \"$l_gpname\" doesn't exist"
  [ -d "$l_gpdir" ] || l_output2="$l_output2\n - The dconf directory \"$l_gpdir\" doesn't exist"

  if [ -n "$l_kfile" ] && grep -Pqrs -- '^\h*automount\h*=\h*false\b' "$l_kfile" 2>/dev/null; then
    :
  else
    l_output2="$l_output2\n - \"automount\" is not set correctly"
  fi

  if [ -n "$l_kfile2" ] && grep -Pqs -- '^\h*automount-open\h*=\h*false\b' "$l_kfile2" 2>/dev/null; then
    :
  else
    l_output2="$l_output2\n - \"automount-open\" is not set correctly"
  fi
else
  l_output2="$l_output2\n - neither \"automount\" or \"automount-open\" is set"
fi

if [ -z "$l_output2" ]; then
  exit $PASS
else
  exit $FAIL
fi