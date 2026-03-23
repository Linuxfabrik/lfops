source /tmp/lib.sh

# tmpfiles systemd.conf: check override/default and perms in file entries are <=0640
l_output="" file_path=""

if [ -f /etc/tmpfiles.d/systemd.conf ]; then
  file_path="/etc/tmpfiles.d/systemd.conf"
elif [ -f /usr/lib/tmpfiles.d/systemd.conf ]; then
  file_path="/usr/lib/tmpfiles.d/systemd.conf"
fi

if [ -z "$file_path" ]; then
  exit $PASS
fi

higher_permissions_found=false

while IFS= read -r line; do
  # skip empty lines and comments
  [[ "$line" =~ ^[[:space:]]*$ ]] && continue
  [[ "$line" =~ ^[[:space:]]*# ]] && continue

  # tmpfiles format: type path mode uid gid age argument...
  # flag any explicit mode that is more permissive than 0640 (e.g. 0641+, 0650+, 0700+, etc)
  if echo "$line" | grep -Piq '^\s*[A-Za-z]\S*\s+\S+\s+0*([6-7][4-7][1-7]|7[0-7][0-7])\s+'; then
    higher_permissions_found=true
    break
  fi
done < "$file_path"

if $higher_permissions_found; then
  exit $FAIL
fi

exit $PASS
