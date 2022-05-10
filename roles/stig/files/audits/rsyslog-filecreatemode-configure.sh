source /tmp/lib.sh

perms=$(grep ^\$FileCreateMode /etc/rsyslog.conf /etc/rsyslog.d/*.conf 2> /dev/null | sed -e 's/^.*:\$FileCreateMode//' -e 's/\s//g')
if [ -z "$perms" ]; then exit $FAIL; fi

u=$(echo $perms | cut -c2)
g=$(echo $perms | cut -c3)
o=$(echo $perms | cut -c4)

if [ $u -gt 6 ]; then exit $FAIL; fi
if [ $g -gt 4 ]; then exit $FAIL; fi
if [ $o -gt 0 ]; then exit $FAIL; fi
exit $PASS
