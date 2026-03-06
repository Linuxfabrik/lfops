source /tmp/lib.sh

if awk -F: 'BEGIN{
  while ((getline < "/etc/shells") > 0) if ($0 ~ /^\// && $0 !~ /nologin/) s=s "|" $0
  sub(/^\|/,"",s); re="^(" s ")$"
}
$7 ~ re { print $1 ":" $6 }' /etc/passwd | while IFS=: read -r u h; do
  [ -d "$h" ] || continue
  g="$(id -gn "$u" | xargs)"
  find "$h" -xdev -type f -name '.*' -print0 2>/dev/null | while IFS= read -r -d $'\0' f; do
    b="$(basename "$f")"
    read -r m o go < <(stat -Lc '%a %U %G' "$f")
    case "$b" in
      .forward|.rhost) exit 1 ;;
      .netrc)
        [ "$o" = "$u" ] || exit 1
        [ "$go" = "$g" ] || exit 1
        (( (8#$m & 0177) == 0 )) || exit 1
        ;;
      .bash_history)
        [ "$o" = "$u" ] || exit 1
        [ "$go" = "$g" ] || exit 1
        (( (8#$m & 0177) == 0 )) || exit 1
        ;;
      *)
        [ "$o" = "$u" ] || exit 1
        [ "$go" = "$g" ] || exit 1
        (( (8#$m & 0133) == 0 )) || exit 1
        ;;
    esac
  done || exit 1
done; then exit $PASS; fi
exit $FAIL
