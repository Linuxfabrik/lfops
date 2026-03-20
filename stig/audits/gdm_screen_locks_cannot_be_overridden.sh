source /tmp/lib.sh

any_pkg_installed "gdm gdm3" || exit $PASS

l_output2=""

# set directory of key file to be locked
l_kfd="/etc/dconf/db/$(grep -Psril '^\h*idle-delay\h*=\h*uint32\h+\d+\b' /etc/dconf/db/*/ 2>/dev/null | awk -F'/' '{split($(NF-1),a,".");print a[1]}' | head -n1).d"
l_kfd2="/etc/dconf/db/$(grep -Psril '^\h*lock-delay\h*=\h*uint32\h+\d+\b' /etc/dconf/db/*/ 2>/dev/null | awk -F'/' '{split($(NF-1),a,".");print a[1]}' | head -n1).d"

if [ -d "$l_kfd" ]; then
  grep -Prilq '\/org\/gnome\/desktop\/session\/idle-delay\b' "$l_kfd" 2>/dev/null || l_output2="$l_output2\n - \"idle-delay\" is not locked"
else
  l_output2="$l_output2\n - \"idle-delay\" is not set so it can not be locked"
fi

if [ -d "$l_kfd2" ]; then
  grep -Prilq '\/org\/gnome\/desktop\/screensaver\/lock-delay\b' "$l_kfd2" 2>/dev/null || l_output2="$l_output2\n - \"lock-delay\" is not locked"
else
  l_output2="$l_output2\n - \"lock-delay\" is not set so it can not be locked"
fi

if [ -z "$l_output2" ]; then
  exit $PASS
else
  exit $FAIL
fi