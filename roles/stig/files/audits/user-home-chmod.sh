source /tmp/lib.sh

for dir in $(grep -E --invert-match '(halt|sync|shutdown|nfsnobody)' /etc/passwd | awk -F: '($7 != "/usr/sbin/nologin" && $7 != "/sbin/nologin" && $7 != "/bin/false") {print $6}' | sort | uniq); do
    perms=$(stat $dir | awk 'NR==4 {print $2}')
    # (0550/dr-xr-x---)
    if [ $(echo $perms | cut -c12) != "-" ]; then exit $FAIL; fi
    if [ $(echo $perms | cut -c14) != "-" ]; then exit $FAIL; fi
    if [ $(echo $perms | cut -c15) != "-" ]; then exit $FAIL; fi
    if [ $(echo $perms | cut -c16) != "-" ]; then exit $FAIL; fi
done
exit $PASS
