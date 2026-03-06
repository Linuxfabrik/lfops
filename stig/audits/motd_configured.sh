source /tmp/lib.sh

l_output2=""
a_files=()

os_id="$(grep '^ID=' /etc/os-release 2>/dev/null | cut -d= -f2 | sed -e 's/"//g')"

for l_file in /etc/motd /etc/motd.d/*; do
  [ -e "$l_file" ] || continue

  if grep -Psqi -- "(\\\v|\\\r|\\\m|\\\s|\b${os_id}\b)" "$l_file"; then
    l_output2="$l_output2\n - File: \"$l_file\" includes system information"
  else
    a_files+=("$l_file")
  fi
done

if [ -z "$l_output2" ]; then
  exit $PASS
else
  exit $FAIL
fi