source /tmp/lib.sh

if nft list ruleset | grep -Pq 'ct state (established|related).*(accept|counter accept)'; then exit $PASS; fi
exit $FAIL
