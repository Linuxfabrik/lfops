source /tmp/lib.sh

l_perm_mask="0137"

if find /etc/audit/ -type f \( -name "*.conf" -o -name '*.rules' \) -perm /"$l_perm_mask" | grep -q '.'; then
  exit $FAIL
fi

exit $PASS
