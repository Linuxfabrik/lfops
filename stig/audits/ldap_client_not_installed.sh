source /tmp/lib.sh

if is_not_installed 'openldap-clients'; then
  exit $PASS
fi
exit $FAIL