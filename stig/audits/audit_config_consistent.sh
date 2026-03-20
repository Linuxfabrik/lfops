source /tmp/lib.sh

augenrules --check 2>&1 | grep -q 'No change' || exit $FAIL

exit $PASS
