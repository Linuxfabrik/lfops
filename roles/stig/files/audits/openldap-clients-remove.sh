source /tmp/lib.sh

if is_installed 'openldap-clients'; then exit $FAIL; fi
exit $PASS
