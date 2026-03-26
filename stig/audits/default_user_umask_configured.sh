source /tmp/lib.sh

umask_ok_re='^\h*umask\h+(0?[0-7][2-7]7|u(=[rwx]{0,3}),g=([rx]{0,2}),o=)(\h*#.*)?$'
umask_bad_re='^\h*umask\h+(([0-7][0-7][01][0-7]\b|[0-7][0-7][0-7][0-6]\b)|([0-7][01][0-7]\b|[0-7][0-7][0-6]\b)|(u=[rwx]{1,3},)?(((g=[rx]?[rx]?w[rx]?[rx]?\b)(,o=[rwx]{1,3})?)|((g=[wrx]{1,3},)?o=[wrx]{1,3}\b)))'

pam_ok_re='^\h*session\h+[^#\n\r]+\h+pam_umask\.so\h+([^#\n\r]+\h+)?umask=(0?[0-7][2-7]7)\b'
pam_bad_re='^\h*session\h+[^#\n\r]+\h+pam_umask\.so\h+([^#\n\r]+\h+)?umask=(([0-7][0-7][01][0-7]\b|[0-7][0-7][0-7][0-6]\b)|([0-7][01][0-7]\b))'

files=()
while IFS= read -r -d $'\0' f; do files+=("$f"); done < <(find /etc/profile.d/ -type f -name '*.sh' -print0 2>/dev/null)
files+=(/etc/profile /etc/bashrc /etc/bash.bashrc /etc/login.defs /etc/default/login)

for f in "${files[@]}"; do
    [ -f "$f" ] || continue
    if grep -Psiq -- "$umask_bad_re" "$f"; then exit $FAIL; fi
done

if [ -f /etc/pam.d/postlogin ]; then
    if grep -Psiq -- "$pam_bad_re" /etc/pam.d/postlogin; then exit $FAIL; fi
fi

for f in "${files[@]}"; do
    [ -f "$f" ] || continue
    if grep -Psiq -- "$umask_ok_re" "$f"; then exit $PASS; fi
done

if [ -f /etc/pam.d/postlogin ]; then
    if grep -Psiq -- "$pam_ok_re" /etc/pam.d/postlogin; then exit $PASS; fi
fi

exit $FAIL