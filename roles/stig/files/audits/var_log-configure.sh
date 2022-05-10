source /tmp/lib.sh

if [ -z "$(mount | grep -E '\s/var/log\s')" ]; then exit $FAIL; fi
exit $PASS
