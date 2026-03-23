source /tmp/lib.sh

any_pkg_installed "gdm gdm3" || exit $PASS

l_output2=""

l_gdmfile="$(grep -Prils '^\h*banner-message-enable\b' /etc/dconf/db/*.d 2>/dev/null | head -n1)"
if [ -n "$l_gdmfile" ]; then
  l_gdmprofile="$(awk -F\/ '{split($(NF-1),a,".");print a[1]}' <<< "$l_gdmfile")"

  grep -Pisq '^\h*banner-message-enable=true\b' "$l_gdmfile" || l_output2="$l_output2\n - The \"banner-message-enable\" option is not enabled"

  l_lsbt="$(grep -Pios '^\h*banner-message-text=.*$' "$l_gdmfile" 2>/dev/null)"
  [ -n "$l_lsbt" ] || l_output2="$l_output2\n - The \"banner-message-text\" option is not set"

  grep -Pq "^\h*system-db:$l_gdmprofile\b" "/etc/dconf/profile/$l_gdmprofile" 2>/dev/null || l_output2="$l_output2\n - The \"$l_gdmprofile\" doesn't exist"

  [ -f "/etc/dconf/db/$l_gdmprofile" ] || l_output2="$l_output2\n - The \"$l_gdmprofile\" profile doesn't exist in the dconf database"
else
  l_output2="$l_output2\n - The \"banner-message-enable\" option isn't configured"
fi

if [ -z "$l_output2" ]; then
  exit $PASS
else
  exit $FAIL
fi