source /tmp/lib.sh

kpname="kernel.randomize_va_space"
expected="2"

runval="$(sysctl -n "$kpname" 2>/dev/null | xargs)"
if [ "$runval" != "$expected" ]; then
  echo "FAIL: $kpname is '$runval' in the running configuration (expected '$expected')"
  exit $FAIL
fi

durable_val=""
durable_file=""

curfile=""

while IFS= read -r line; do
  if echo "$line" | grep -Pq '^\s*#\s*/[^#\s]+\.conf\b'; then
    curfile="${line#\# }"
    curfile="$(echo "$curfile" | xargs)"
    continue
  fi

  echo "$line" | grep -Pq '^\s*#' && continue
  [ -z "$(echo "$line" | xargs)" ] && continue

  if echo "$line" | grep -Pq "^\s*${kpname//./\\.}\s*="; then
    durable_val="$(echo "$line" | awk -F= '{print $2}' | xargs)"
    durable_file="$curfile"
  fi
done < <(/usr/lib/systemd/systemd-sysctl --cat-config 2>/dev/null)

ufwscf=""
if [ -f /etc/default/ufw ]; then
  ufwscf="$(awk -F= '/^\s*IPT_SYSCTL=/ {print $2}' /etc/default/ufw | xargs)"
fi

if [ -n "$ufwscf" ] && [ -f "$ufwscf" ]; then
  ufw_last="$(grep -P "^\s*${kpname//./\\.}\s*=" "$ufwscf" 2>/dev/null | tail -n 1)"
  if [ -n "$ufw_last" ]; then
    durable_val="$(echo "$ufw_last" | awk -F= '{print $2}' | xargs)"
    durable_file="$ufwscf"
  fi
fi

if [ -z "$durable_val" ]; then
  echo "FAIL: $kpname is not set in an included sysctl configuration file"
  exit $FAIL
fi

if [ "$durable_val" != "$expected" ]; then
  echo "FAIL: $kpname is '$durable_val' in '$durable_file' (expected '$expected')"
  exit $FAIL
fi

echo "PASS: $kpname is '$expected' in running config and durable config ($durable_file)"
exit $PASS