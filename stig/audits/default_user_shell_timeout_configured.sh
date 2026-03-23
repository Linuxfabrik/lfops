source /tmp/lib.sh

l_tmout_set="900"
l_found=0

while IFS= read -r l_file; do
  l_tmout_value="$(grep -Po -- '^([^#\n\r]+)?\bTMOUT=\d+\b' "$l_file" | awk -F= '{print $2}')"
  [ -z "$l_tmout_value" ] && continue
  if [[ "$l_tmout_value" -gt "$l_tmout_set" || "$l_tmout_value" -le "0" ]]; then
    exit $FAIL
  fi
  grep -Pq -- '^\h*(typeset\h\-xr\hTMOUT=\d+|([^#\n\r]+)?\breadonly\h+TMOUT\b)' "$l_file" || exit $FAIL
  grep -Pq -- '^\h*(typeset\h\-xr\hTMOUT=\d+|([^#\n\r]+)?\bexport\b([^#\n\r]+\b)?TMOUT\b)' "$l_file" || exit $FAIL
  l_found=1
done < <(grep -Pls -- '^([^#\n\r]+)?\bTMOUT\b' /etc/*bashrc /etc/profile /etc/profile.d/*.sh 2>/dev/null)

if [ "$l_found" -eq 0 ]; then
  exit $FAIL
fi

exit $PASS
