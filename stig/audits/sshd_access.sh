source /tmp/lib.sh

if grep -Pi '^\h*(AllowUsers|AllowGroups|DenyUsers|DenyGroups)\h+\S+' /etc/ssh/sshd_config /etc/ssh/sshd_config.d/*.conf 2>/dev/null; then exit $PASS; fi
exit $FAIL
