source /tmp/lib.sh

if [ -z "$(mount | grep -E '\s/home\s')" ]; then exit $FAIL; fi
exit $PASS
