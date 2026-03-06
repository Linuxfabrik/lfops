source /tmp/lib.sh

any_pkg_installed "gdm gdm3" || exit $PASS

l_output2=""

l_kfd="/etc/dconf/db/$(grep -Psril '^\h*automount\b' /etc/dconf/db/*/ 2>/dev/null | awk -F'/' '{split($(NF-1),a,".");print a[1]}' | head -n1).d"
l_kfd2="/etc/dconf/db/$(grep -Psril '^\h*automount-open\b' /etc/dconf/db/*/ 2>/dev/null | awk -F'/' '{split($(NF-1),a,".");print a[1]}' | head -n1).d"

if [ -d "$l_kfd" ]; then
  if grep -Priq '^\h*\/org\/gnome\/desktop\/media-handling\/automount\b' "$l_kfd" 2>/dev/null; then
    :
  else
    l_output2="$l_output2\n - \"automount\" is not locked"
  fi
else
  l_output2="$l_output2\n - \"automount\" is not set so it can not be locked"
fi

if [ -d "$l_kfd2" ]; then
  if grep -Priq '^\h*\/org\/gnome\/desktop\/media-handling\/automount-open\b' "$l_kfd2" 2>/dev/null; then
    :
  else
    l_output2="$l_output2\n - \"automount-open\" is not locked"
  fi
else
  l_output2="$l_output2\n - \"automount-open\" is not set so it can not be locked"
fi

if [ -z "$l_output2" ]; then
  exit $PASS
else
  exit $FAIL
fi
