source /tmp/lib.sh

if [ $(grep -E --count "^auth\s+required\s+pam_wheel.so\s+use_uid" /etc/pam.d/su) -eq 0 ]; then exit $FAIL; fi
exit $PASS
