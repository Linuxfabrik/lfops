source /tmp/lib.sh

any_pkg_installed "gdm gdm3" || exit $PASS

l_output2=""
l_idmv="900" # Set for max value for idle-delay in seconds
l_ldmv="5"   # Set for max value for lock-delay in seconds

# Determine file containing idle-delay key
l_kfile="$(grep -Psril '^\h*idle-delay\h*=\h*uint32\h+\d+\b' /etc/dconf/db/*/ 2>/dev/null | head -n1)"

if [ -n "$l_kfile" ]; then
  # set profile name (This is the name of a dconf database)
  l_profile="$(awk -F'/' '{split($(NF-1),a,".");print a[1]}' <<< "$l_kfile")"

  # Confirm that idle-delay exists, includes uint32, and value is between 1 and max
  l_idv="$(awk -F 'uint32' '/idle-delay/{print $2}' "$l_kfile" 2>/dev/null | xargs)"
  if [ -n "$l_idv" ]; then
    [ "$l_idv" -gt "0" -a "$l_idv" -le "$l_idmv" ] || l_output2="$l_output2\n - The \"idle-delay\" option is not set correctly"
  else
    l_output2="$l_output2\n - The \"idle-delay\" option is not set in \"$l_kfile\""
  fi

  # Confirm that lock-delay exists, includes uint32, and value is between 0 and max
  l_ldv="$(awk -F 'uint32' '/lock-delay/{print $2}' "$l_kfile" 2>/dev/null | xargs)"
  if [ -n "$l_ldv" ]; then
    [ "$l_ldv" -ge "0" -a "$l_ldv" -le "$l_ldmv" ] || l_output2="$l_output2\n - The \"lock-delay\" option is not set correctly"
  else
    l_output2="$l_output2\n - The \"lock-delay\" option is not set in \"$l_kfile\""
  fi

  # Confirm that dconf profile exists
  grep -Psq "^\h*system-db:$l_profile\b" /etc/dconf/profile/* 2>/dev/null || l_output2="$l_output2\n - The \"$l_profile\" doesn't exist"

  # Confirm that dconf profile database file exists
  [ -f "/etc/dconf/db/$l_profile" ] || l_output2="$l_output2\n - The \"$l_profile\" profile doesn't exist in the dconf database"
else
  l_output2="$l_output2\n - The \"idle-delay\" option doesn't exist, remaining tests skipped"
fi

if [ -z "$l_output2" ]; then
  exit $PASS
else
  exit $FAIL
fi