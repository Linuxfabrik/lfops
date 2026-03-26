source /tmp/lib.sh

fail=0

UID_MIN=$(awk '/^\s*UID_MIN/{print $2}' /etc/login.defs)
[ -n "${UID_MIN}" ] || exit $FAIL

# syscall rules
awk '/^ *-a *always,exit/ \
&&/ -F *arch=b(32|64)/ \
&&(/ -F auid!=unset/||/ -F auid!=-1/||/ -F auid!=4294967295/) \
&&/ -S/ \
&&(/init_module/ \
 ||/finit_module/ \
 ||/delete_module/ \
 ||/create_module/ \
 ||/query_module/) \
&&(/ key= *[!-~]* *$/||/ -k *[!-~]* *$/)' /etc/audit/rules.d/*.rules | grep -q '.' || fail=1

awk "/^ *-a *always,exit/ \
&&(/ -F *auid!=unset/||/ -F *auid!=-1/||/ -F *auid!=4294967295/) \
&&/ -F *auid>=${UID_MIN}/ \
&&/ -F *perm=x/ \
&&/ -F *path=\/usr\/bin\/kmod/ \
&&(/ key= *[!-~]* *$/||/ -k *[!-~]* *$/)" /etc/audit/rules.d/*.rules | grep -q '.' || fail=1

# running config
auditctl -l | awk '/^ *-a *always,exit/ \
&&/ -F *arch=b(32|64)/ \
&&(/ -F auid!=unset/||/ -F auid!=-1/||/ -F auid!=4294967295/) \
&&/ -S/ \
&&(/init_module/ \
 ||/finit_module/ \
 ||/delete_module/ \
 ||/create_module/ \
 ||/query_module/) \
&&(/ key= *[!-~]* *$/||/ -k *[!-~]* *$/)' | grep -q '.' || fail=1

auditctl -l | awk "/^ *-a *always,exit/ \
&&(/ -F *auid!=unset/||/ -F *auid!=-1/||/ -F *auid!=4294967295/) \
&&/ -F *auid>=${UID_MIN}/ \
&&/ -F *perm=x/ \
&&/ -F *path=\/usr\/bin\/kmod/ \
&&(/ key= *[!-~]* *$/||/ -k *[!-~]* *$/)" | grep -q '.' || fail=1

if [ "$fail" -eq 0 ]; then
  exit $PASS
else
  exit $FAIL
fi
