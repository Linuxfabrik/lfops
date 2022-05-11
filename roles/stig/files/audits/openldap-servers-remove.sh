source /tmp/lib.sh

if is_installed 'openldap-servers'; then exit $FAIL; fi
exit $PASS
