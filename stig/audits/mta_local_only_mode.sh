source /tmp/lib.sh

if [ "$(postconf -n inet_interfaces 2>/dev/null)" != "inet_interfaces = all" ] && ! ss -plntu | grep -P -- ':(25|465|587)\b' | grep -Pvq -- '\h+(127\.0\.0\.1|\[?::1\]?):(25|465|587)\b'; then exit $PASS; fi
exit $FAIL
