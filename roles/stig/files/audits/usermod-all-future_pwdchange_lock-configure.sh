source /tmp/lib.sh

for user in $(cat /etc/shadow | cut -d: -f1); do
    change_date=$(chage --list $user | sed -n '/Last password change/ s/^.*: //p')
    if [ "$change_date" != 'never' ]; then
        if [ $(date -d "$change_date" +%s) -gt $(date +%s) ]; then exit $FAIL; fi
    fi
done
exit $PASS
