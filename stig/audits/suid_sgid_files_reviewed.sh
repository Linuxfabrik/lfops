source /tmp/lib.sh

if ! while IFS= read -r l_mount; do find "$l_mount" -xdev -type f \( -perm -2000 -o -perm -4000 \) -print 2>/dev/null; done < <(findmnt -Dkerno fstype,target,options | awk '($1 !~ /^\s*(nfs|proc|smb|vfat|iso9660|efivarfs|selinuxfs)/ && $2 !~ /^\/run\/user\// && $3 !~/noexec/ && $3 !~/nosuid/) {print $2}'); do :; done | grep -q .; then exit $PASS; fi
exit $FAIL
