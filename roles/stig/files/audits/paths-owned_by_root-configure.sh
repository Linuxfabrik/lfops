source /tmp/lib.sh

if [ $(echo $PATH | grep --count '::') -ne 0 ]; then exit $FAIL; fi
if [ $(echo $PATH | grep --count ':$') -ne 0 ]; then exit $FAIL; fi
for p in $(echo $PATH | sed -e 's/:/ /g'); do
    if [ -d $p ]; then
        if [ "$p" == "." ]; then exit $FAIL; fi
        perms=$(ls -hald "$p/")
        if [ "$(echo $perms | cut -c6)" != '-' ]; then exit $FAIL; fi
        if [ "$(echo $perms | cut -c9)" != '-' ]; then exit $FAIL; fi
        if [ "$(echo $perms | awk '{print $3}')" != "root" ]; then exit $FAIL; fi
    fi
done
exit $PASS
