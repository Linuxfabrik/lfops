source /tmp/lib.sh

masks=$(awk '/^(\s+)?umask\s+[0-7]{3}/ {print $2}' /etc/bashrc /etc/profile /etc/profile.d/*.sh)
if [ -z "$masks" ]; then exit $FAIL; fi
for mask in $masks; do
    bits=($(echo $mask | grep --only-matching .))
    if [ ${bits[0]} -lt 0 ]; then exit $FAIL; fi
    if [ ${bits[1]} -lt 2 ]; then exit $FAIL; fi
    if [ ${bits[2]} -lt 7 ]; then exit $FAIL; fi
done
exit $PASS
