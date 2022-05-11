source /tmp/lib.sh

if is_installed 'gdm'; then exit $FAIL; fi
exit $PASS
