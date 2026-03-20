source /tmp/lib.sh

l_output2=""
l_pmask="0022"
l_maxperm="$( printf '%o' $(( 0777 & ~$l_pmask )) )"
l_root_path="$(sudo -Hiu root env | grep '^PATH' | cut -d= -f2)"

unset a_path_loc && IFS=":" read -ra a_path_loc <<< "$l_root_path"

grep -q "::" <<< "$l_root_path" && l_output2="fail"
grep -Pq ":\h*$" <<< "$l_root_path" && l_output2="fail"
grep -Pq '(\h+|:)\.(:|\h*$)' <<< "$l_root_path" && l_output2="fail"

while read -r l_path; do
    if [ -d "$l_path" ]; then
        while read -r l_fmode l_fown; do
            [ "$l_fown" != "root" ] && l_output2="fail"
            [ $(( l_fmode & l_pmask )) -gt 0 ] && l_output2="fail"
        done <<< "$(stat -Lc '%#a %U' "$l_path" 2>/dev/null)"
    else
        l_output2="fail"
    fi
done <<< "$(printf "%s\n" "${a_path_loc[@]}")"

if [ -z "$l_output2" ]; then
    exit $PASS
fi

exit $FAIL