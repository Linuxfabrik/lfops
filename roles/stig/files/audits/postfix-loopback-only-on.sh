source /tmp/lib.sh

if [ -z "$(ss -lntu | grep -E ':25\s')" ]; then exit $SKIP; fi
if [ -n "$(ss -lntu | grep -E ':25\s' | grep -E --invert-match '\s(127.0.0.1:25|\[::1]:25)\s')" ]; then exit $FAIL; fi
exit $PASS
