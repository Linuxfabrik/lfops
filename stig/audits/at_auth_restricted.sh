source /tmp/lib.sh

# not applicable if at not installed
is_not_installed at && exit $PASS

# /etc/at.allow must exist, mode <=640, owner root, group root or daemon
[ -f /etc/at.allow ] || exit $FAIL
mode="$(stat -Lc '%a' /etc/at.allow 2>/dev/null)"
uid="$(stat -Lc '%u' /etc/at.allow 2>/dev/null)"
grp="$(stat -Lc '%G' /etc/at.allow 2>/dev/null)"
[ "$mode" -le 640 ] && [ "$uid" -eq 0 ] && [[ "$grp" == "root" || "$grp" == "daemon" ]] || exit $FAIL

# /etc/at.deny: must not exist, or be mode <=640, owner root, group root or daemon
if [ -e /etc/at.deny ]; then
  mode="$(stat -Lc '%a' /etc/at.deny 2>/dev/null)"
  uid="$(stat -Lc '%u' /etc/at.deny 2>/dev/null)"
  grp="$(stat -Lc '%G' /etc/at.deny 2>/dev/null)"
  [ "$mode" -le 640 ] && [ "$uid" -eq 0 ] && [[ "$grp" == "root" || "$grp" == "daemon" ]] || exit $FAIL
fi

exit $PASS
