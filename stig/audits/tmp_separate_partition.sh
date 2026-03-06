source /tmp/lib.sh

if findmnt -kn /tmp >/dev/null 2>&1 && ! systemctl is-enabled tmp.mount 2>/dev/null | grep -Eq 'masked|disabled'; then exit $PASS; fi
exit $FAIL
