source /tmp/lib.sh

audit_lines=$(rpm --verify --all --nomtime --nosize --nomd5 --nolinkto)
# ignore all the files we will harden/change permissions while applying all the remediations
audit_lines=$(echo "$audit_lines" | sed '/\/boot\/grub2\/grub.cfg/d')
audit_lines=$(echo "$audit_lines" | sed '/\/etc\/gshadow/d')
audit_lines=$(echo "$audit_lines" | sed '/\/etc\/issue/d')
audit_lines=$(echo "$audit_lines" | sed '/\/etc\/motd/d')
audit_lines=$(echo "$audit_lines" | sed '/\/etc\/shadow/d')
audit_lines=$(echo "$audit_lines" | sed '/\/var\/log/d')
if [ -n "$audit_lines" ]; then
    echo rpm verify system file permissions of all installed packages
    echo ------------------------------------------------------------
    echo ''
    echo "$audit_lines"
    echo ''
    exit $REV
fi
exit $PASS
