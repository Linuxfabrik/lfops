source /tmp/lib.sh

if awk -F: 'BEGIN{
  while ((getline < "/etc/shells") > 0) if ($0 ~ /^\// && $0 !~ /nologin/) s=s "|" $0
  sub(/^\|/,"",s); re="^(" s ")$"
}
$7 ~ re { print $1 ":" $6 }' /etc/passwd | while IFS=: read -r u h; do
  [ -d "$h" ] || exit 1
  [ "$(stat -Lc '%U' "$h")" = "$u" ] || exit 1
  m="$(stat -Lc '%a' "$h")"
  (( (8#$m & 0027) == 0 )) || exit 1
done; then exit $PASS; fi
exit $FAIL
