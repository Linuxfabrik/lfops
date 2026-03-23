source /tmp/lib.sh

any_pkg_installed "gdm gdm3" || exit $PASS

output2=""

l_gdmfile="$(grep -Pril '^\h*disable-user-list\h*=\h*true\b' /etc/dconf/db 2>/dev/null | head -n1)"
if [ -n "$l_gdmfile" ]; then
  l_gdmprofile="$(awk -F\/ '{split($(NF-1),a,".");print a[1]}' <<< "$l_gdmfile")"

  grep -Pq "^\h*system-db:$l_gdmprofile\b" "/etc/dconf/profile/$l_gdmprofile" 2>/dev/null || output2="$output2\n - The \"$l_gdmprofile\" doesn't exist"
  [ -f "/etc/dconf/db/$l_gdmprofile" ] || output2="$output2\n - The \"$l_gdmprofile\" profile doesn't exist in the dconf database"
else
  output2="$output2\n - The \"disable-user-list\" option is not enabled"
fi

if [ -z "$output2" ]; then
  exit $PASS
else
  exit $FAIL
fi