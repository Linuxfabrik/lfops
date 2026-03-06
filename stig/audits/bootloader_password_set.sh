source /tmp/lib.sh      

l_grub_password_file="$(find /boot -type f -name 'user.cfg' ! -empty)"

if [ -f "$l_grub_password_file" ] && \
   awk -F. '/^\s*GRUB2_PASSWORD=\S+/ {print $1"."$2"."$3}' "$l_grub_password_file" | \
   grep -q '^GRUB2_PASSWORD=grub\.pbkdf2\.sha512'; then
  exit $PASS
fi

exit $FAIL
