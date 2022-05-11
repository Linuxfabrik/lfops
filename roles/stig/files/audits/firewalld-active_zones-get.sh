source /tmp/lib.sh

if is_not_installed 'firewalld'; then exit $SKIP; fi
if is_disabled 'firewalld'; then exit $SKIP; fi
audit_lines=$(nmcli -t connection show | awk -F: '{if($4){print $4}}' | while read INT; do firewall-cmd --get-active-zones | grep -B1 $INT; done)
echo firewalld active zones
echo ----------------------
echo ''
echo "$audit_lines"
echo ''
exit $REV
