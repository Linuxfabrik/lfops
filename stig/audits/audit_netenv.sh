source /tmp/lib.sh

fail=0

awk '/^ *-a *always,exit/ \
&&/ -F *arch=b(32|64)/ \
&&/ -S/ \
&&(/sethostname/ \
||/setdomainname/) \
&&(/ key= *[!-~]* *$/||/ -k *[!-~]* *$/)' /etc/audit/rules.d/*.rules | grep -q '.' || fail=1

awk '/^ *-w/ \
&&(/\/etc\/issue/ \
||/\/etc\/issue.net/ \
||/\/etc\/hosts/ \
||/\/etc\/sysconfig\/network/ \
||/\/etc\/hostname/ \
||/\/etc\/NetworkManager/) \
&&/ +-p *wa/ \
&&(/ key= *[!-~]* *$/||/ -k *[!-~]* *$/)' /etc/audit/rules.d/*.rules | grep -q '.' || fail=1

auditctl -l | awk '/^ *-a *always,exit/ \
&&/ -F *arch=b(32|64)/ \
&&/ -S/ \
&&(/sethostname/ \
||/setdomainname/) \
&&(/ key= *[!-~]* *$/||/ -k *[!-~]* *$/)' | grep -q '.' || fail=1

auditctl -l | awk '/^ *-w/ \
&&(/\/etc\/issue/ \
||/\/etc\/issue.net/ \
||/\/etc\/hosts/ \
||/\/etc\/sysconfig\/network/ \
||/\/etc\/hostname/ \
||/\/etc\/NetworkManager/) \
&&/ +-p *wa/ \
&&(/ key= *[!-~]* *$/||/ -k *[!-~]* *$/)' | grep -q '.' || fail=1

if [ "$fail" -eq 0 ]; then
  exit $PASS
else
  exit $FAIL
fi