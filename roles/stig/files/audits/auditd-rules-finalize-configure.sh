source /tmp/lib.sh

if [ "$(grep "^\s*[^#]" /etc/audit/rules.d/*.rules | tail -n1 | sed -e 's/^.*://')" == '-e 2' ]; then exit $PASS; fi
if [ "$(grep "^\s*[^#]" /etc/audit/audit.rules | tail -n1 | sed 's/^\s*//')" == '-e 2' ]; then exit $PASS; fi
exit $FAIL
