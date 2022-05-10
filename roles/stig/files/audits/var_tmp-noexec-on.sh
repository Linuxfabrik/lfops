source /tmp/lib.sh

if [ -z "$(mount | grep -E '\s/var/tmp\s')" ]; then exit $SKIP; fi
if [ -n "$(mount | grep -E '\s/var/tmp\s' | grep --invert-match noexec)" ]; then exit $FAIL; fi
exit $PASS
