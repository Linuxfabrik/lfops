source /tmp/lib.sh

if is_installed 'audit' && is_installed 'audit-libs'; then
    exit $PASS
fi
exit $FAIL