source /tmp/lib.sh

fail=0

SUDO_LOG_FILE=$(grep -r logfile /etc/sudoers* | sed -e 's/.*logfile=//;s/,? .*//' -e 's/"//g' -e 's|/|\\/|g')
[ -n "${SUDO_LOG_FILE}" ] || exit $FAIL

awk "/^ *-w/ \
&&/${SUDO_LOG_FILE}/ \
&&/ +-p *wa/ \
&&(/ key= *[!-~]* *$/||/ -k *[!-~]* *$/)" /etc/audit/rules.d/*.rules | grep -q '.' || fail=1

auditctl -l | awk "/^ *-w/ \
&&/${SUDO_LOG_FILE}/ \
&&/ +-p *wa/ \
&&(/ key= *[!-~]* *$/||/ -k *[!-~]* *$/)" | grep -q '.' || fail=1

if [ "$fail" -eq 0 ]; then
  exit $PASS
else
  exit $FAIL
fi