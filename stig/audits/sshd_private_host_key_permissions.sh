source /tmp/lib.sh

l_output="" l_output2=""

# Determine ssh key group name if present (ssh_keys, ssh, _ssh)
l_ssh_group_name="$(awk -F: '($1 ~ /^(ssh_keys|_?ssh)$/) {print $1; exit}' /etc/group)"

f_file_chk() {
while IFS=: read -r l_file_mode l_file_owner l_file_group; do
    l_out2=""

    # If group is the SSH key group allow group-read; else stricter (no group perms)
    if [ -n "$l_ssh_group_name" ] && [ "$l_file_group" = "$l_ssh_group_name" ]; then
    l_pmask="0137"
    else
    l_pmask="0177"
    fi

    l_maxperm="$(printf '%o' $(( 0777 & ~${l_pmask#0} )))"

    # mode too permissive (treat as octal)
    if [ $(( 8#$l_file_mode & 8#$l_pmask )) -gt 0 ]; then
    l_out2="$l_out2\n - Mode: \"$l_file_mode\" should be mode: \"$l_maxperm\" or more restrictive"
    fi

    # wrong owner
    if [ "$l_file_owner" != "root" ]; then
    l_out2="$l_out2\n - Owned by: \"$l_file_owner\" should be owned by \"root\""
    fi

    # wrong group (root or ssh group)
    if [ -n "$l_ssh_group_name" ]; then
    if [[ ! "$l_file_group" =~ ^($l_ssh_group_name|root)$ ]]; then
        l_out2="$l_out2\n - Owned by group: \"$l_file_group\" should be group owned by: \"$l_ssh_group_name\" or \"root\""
    fi
    else
    if [ "$l_file_group" != "root" ]; then
        l_out2="$l_out2\n - Owned by group: \"$l_file_group\" should be group owned by: \"root\""
    fi
    fi

    if [ -n "$l_out2" ]; then
    l_output2="$l_output2\n - File: \"$l_file\"$l_out2"
    else
    l_output="$l_output\n - File: \"$l_file\"\n - Correct: mode: \"$l_file_mode\", owner: \"$l_file_owner\", and group owner: \"$l_file_group\" configured"
    fi
done < <(stat -Lc '%a:%U:%G' "$l_file" 2>/dev/null)
}

while IFS= read -r -d $'\0' l_file; do
if ssh-keygen -lf "$l_file" &>/dev/null; then
    if file "$l_file" | grep -Piq -- '\bopenssh\h+([^#\n\r]+\h+)?private\h+key\b'; then
    f_file_chk
    fi
fi
done < <(find -L /etc/ssh -xdev -type f -print0 2>/dev/null)

if [ -z "$l_output2" ]; then
[ -z "$l_output" ] && l_output="\n - No OpenSSH private keys found"
echo -e "\n- Audit Result:\n ** PASS **\n - * Correctly configured * :$l_output"
exit $PASS
else
echo -e "\n- Audit Result:\n ** FAIL **\n - * Reasons for audit failure * :$l_output2\n"
[ -n "$l_output" ] && echo -e "\n - * Correctly configured * :\n$l_output\n"
exit $FAIL
fi
