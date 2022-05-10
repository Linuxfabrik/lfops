source /tmp/lib.sh

if [ -z "$(mount | grep -E '\s/tmp\s')" ]; then exit $SKIP; fi
if [ -n "$(mount | grep -E '\s/tmp\s' | grep --invert-match nosuid)" ]; then exit $FAIL; fi
exit $PASS
