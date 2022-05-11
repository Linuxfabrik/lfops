source /tmp/lib.sh

if is_not_installed 'firewalld'; then exit $SKIP; fi
if is_disabled 'firewalld'; then exit $SKIP; fi
audit_lines=$(firewall-cmd --get-default-zone)
echo firewalld default zone
echo ----------------------
echo ''
echo "$audit_lines"
echo ''
exit $REV
