source /tmp/lib.sh

if test_perms 600 '/etc/ssh/sshd_config'; then exit $PASS; fi
exit $FAIL
