source /tmp/lib.sh

if systemctl --quiet is-enabled nftables.service && ! nft list ruleset | grep 'hook input' | grep -v 'policy drop' | grep -q . && ! nft list ruleset | grep 'hook forward' | grep -v 'policy drop' | grep -q .; then exit $PASS; fi
exit $FAIL
