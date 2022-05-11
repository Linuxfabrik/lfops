source /tmp/lib.sh

search_term='scope'
# is the order always the same? add sort? TODO: do this for all diffs
expected='-w /etc/sudoers -p wa -k scope\n
    -w /etc/sudoers.d -p wa -k scope'
if diff <(echo -e $expected | sed 's/^\s*//' | sort) <(auditctl -l | grep $search_term | sort) &>/dev/null; then exit $PASS; fi
exit $FAIL
