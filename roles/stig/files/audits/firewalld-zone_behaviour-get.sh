source /tmp/lib.sh

if is_not_installed 'firewalld'; then exit $SKIP; fi
if is_disabled 'firewalld'; then exit $SKIP; fi
audit_lines=$(firewall-cmd --get-active-zones | awk '!/:/ {print $1}' | while read ZN; do firewall-cmd --list-all --zone=$ZN; done)
echo firewalld target behaviour of every zone
echo ----------------------------------------
echo ''
echo "$audit_lines"
echo ''
exit $REV
