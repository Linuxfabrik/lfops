source /tmp/lib.sh

if [ -z "$(mount | grep -E '\s/tmp\s')" ]; then exit $SKIP; fi
if [ -n "$(mount | grep -E '\s/tmp\s' | grep --invert-match nodev)" ]; then exit $FAIL; fi
if [ -n "$(mount | grep -E '\s/tmp\s' | grep --invert-match noexec)" ]; then exit $FAIL; fi
if [ -n "$(mount | grep -E '\s/tmp\s' | grep --invert-match nosuid)" ]; then exit $FAIL; fi
if [ -n "$(systemctl show 'tmp.mount' | grep -i unitfilestate)" ]; then exit $PASS; fi
exit $FAIL
