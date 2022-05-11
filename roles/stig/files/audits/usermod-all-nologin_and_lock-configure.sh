source /tmp/lib.sh

# changed
# && $7!="'"$(which nologin)"'
# into
# && $7!="/sbin/nologin" && $7!="/usr/sbin/nologin"
if [ $(awk -F: '($1!="root" && $1!="sync" && $1!="shutdown" && $1!="halt" && $1!~/^\+/ && $3<'"$(awk '/^\s*UID_MIN/{print $2}' /etc/login.defs)"' && $7!="/sbin/nologin" && $7!="/usr/sbin/nologin" && $7!="/bin/false") {print}' /etc/passwd | wc -l) -ne 0 ]; then exit $FAIL; fi
if [ $(awk -F: '($1!="root" && $1!~/^\+/ && $3<'"$(awk '/^\s*UID_MIN/{print $2}' /etc/login.defs)"') {print $1}' /etc/passwd | xargs -I '{}' passwd -S '{}' | awk '($2!="L" && $2!="LK") {print $1}') ]; then exit $FAIL; fi
exit $PASS
