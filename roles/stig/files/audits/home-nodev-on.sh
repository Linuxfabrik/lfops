source /tmp/lib.sh

if [ -z "$(mount | grep -E '\s/home\s')" ]; then exit $SKIP; fi
if [ -n "$(mount | grep -E '\s/home\s' | grep --invert-match nodev)" ]; then exit $FAIL; fi
exit $PASS
