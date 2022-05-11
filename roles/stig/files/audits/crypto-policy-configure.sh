source /tmp/lib.sh

crypto_policy=$(grep -E -i '^\s*(FUTURE|FIPS)\s*(\s+#.*)?$' /etc/crypto-policies/config 2> /dev/null)
if [ "$crypto_policy" == 'FUTURE' ]; then exit $PASS; fi
if [ "$crypto_policy" == 'FIPS' ]; then exit $PASS; fi
exit $FAIL
