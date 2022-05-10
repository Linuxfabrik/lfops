source /tmp/lib.sh

audit_lines=$(yum repolist)
echo yum repolist
echo ------------
echo ''
echo "$audit_lines"
echo ''
exit $REV
