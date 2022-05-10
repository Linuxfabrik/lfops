source /tmp/lib.sh

if ! command -v nmcli &> /dev/null; then exit $SKIP; fi
if [ "$(nmcli radio all | tail -1 | xargs)" == 'enabled disabled enabled disabled' ]; then exit $PASS; fi
exit $FAIL
