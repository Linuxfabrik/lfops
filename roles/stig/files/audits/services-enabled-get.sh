source /tmp/lib.sh

audit_lines=$(systemctl list-unit-files --type service --state enabled --no-legend)
echo list of current services enabled
echo --------------------------------
echo ''
echo "$audit_lines"
echo ''
exit $REV
