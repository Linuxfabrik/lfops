source /tmp/lib.sh

file_path=""
if [ -f /etc/tmpfiles.d/systemd.conf ]; then
  file_path="/etc/tmpfiles.d/systemd.conf"
elif [ -f /usr/lib/tmpfiles.d/systemd.conf ]; then
  file_path="/usr/lib/tmpfiles.d/systemd.conf"
fi

if [ -n "$file_path" ]; then
  if ! stat -Lc '%a' "$file_path" | grep -Eq '^(0|2|4|6)40$'; then
    exit $FAIL
  fi
  exit $PASS
fi

exit $PASS
