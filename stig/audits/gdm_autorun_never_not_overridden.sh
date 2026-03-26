source /tmp/lib.sh

any_pkg_installed "gdm gdm3" || exit $PASS

l_output2=""

l_kfd="/etc/dconf/db/$(grep -Psril '^\h*autorun-never\b' /etc/dconf/db/*/ 2>/dev/null | awk -F'/' '{split($(NF-1),a,".");print a[1]}' | head -n1).d"

if [ -d "$l_kfd" ]; then
  grep -Priq '^\h*\/org\/gnome\/desktop\/media-handling\/autorun-never\b' "$l_kfd" 2>/dev/null || l_output2="$l_output2\n - \"autorun-never\" is not locked"
else
  l_output2="$l_output2\n - \"autorun-never\" is not set so it can not be locked"
fi

if [ -z "$l_output2" ]; then
  exit $PASS
else
  exit $FAIL
fi