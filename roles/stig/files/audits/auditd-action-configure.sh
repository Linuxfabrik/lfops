source /tmp/lib.sh

if [ $(grep --count '^space_left_action\s*=\s*email' /etc/audit/auditd.conf) -eq 1 ]; then exit $PASS; fi
if [ $(grep --count '^action_mail_acct\s*=\s*root' /etc/audit/auditd.conf) -eq 1 ]; then exit $PASS; fi
if [ $(grep --count '^admin_space_left_action\s*=\s*halt' /etc/audit/auditd.conf) -eq 1 ]; then exit $PASS; fi
exit $FAIL
