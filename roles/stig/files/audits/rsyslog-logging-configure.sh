source /tmp/lib.sh

audit_lines=$(ls -l /var/log/)
echo Ensure logging is configured
echo ----------------------------
echo ''
echo "$audit_lines"
echo ''
exit $REV
