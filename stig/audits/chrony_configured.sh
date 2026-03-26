source /tmp/lib.sh      

if is_installed 'chrony'; then
    if grep -Prs -- '^\h*(server|pool)\h+[^#\n\r]+' /etc/chrony.conf /etc/chrony.d/ &>/dev/null; then
        exit $PASS
    fi
fi
exit $FAIL