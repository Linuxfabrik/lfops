source /tmp/lib.sh

audit_lines=$(dnf repolist)
echo dnf repolist
echo ------------
echo ''
echo "$audit_lines"
echo ''
exit $REV
