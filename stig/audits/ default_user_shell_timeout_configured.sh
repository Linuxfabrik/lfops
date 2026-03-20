source /tmp/lib.sh

l_tmout_set="900"
files="$(grep -Pls -- '^([^#\n\r]+)?\bTMOUT\b' /etc/*bashrc /etc/profile /etc/profile.d/*.sh 2>/dev/null)"

[ -n "$files" ] || exit $FAIL

found_ok=""

while IFS= read -r f; do
    [ -f "$f" ] || continue

    tmout_vals="$(grep -Po -- '^([^#\n\r]+)?\bTMOUT=\d+\b' "$f" 2>/dev/null | awk -F= '{print $2}')"
    tmout_readonly="$(grep -P -- '^\h*(typeset\h\-xr\hTMOUT=\d+|([^#\n\r]+)?\breadonly\h+TMOUT\b)' "$f" 2>/dev/null)"
    tmout_export="$(grep -P -- '^\h*(typeset\h\-xr\hTMOUT=\d+|([^#\n\r]+)?\bexport\b([^#\n\r]+\b)?TMOUT\b)' "$f" 2>/dev/null)"

    if [ -n "$tmout_vals" ]; then
        while IFS= read -r v; do
            [ -n "$v" ] || continue

            if [ "$v" -le 0 ] || [ "$v" -gt "$l_tmout_set" ]; then
                exit $FAIL
            fi

            if [ -z "$tmout_readonly" ] || [ -z "$tmout_export" ]; then
                exit $FAIL
            fi

            found_ok="1"
        done <<< "$tmout_vals"
    else
        if [ -n "$tmout_readonly" ] || [ -n "$tmout_export" ]; then
            exit $FAIL
        fi
    fi
done <<< "$files"

[ -n "$found_ok" ] || exit $FAIL

exit $PASS