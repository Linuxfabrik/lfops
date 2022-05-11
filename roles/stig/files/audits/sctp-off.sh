source /tmp/lib.sh

if is_active_kernelmod 'sctp'; then exit $FAIL; fi
exit $PASS
