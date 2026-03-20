source /tmp/lib.sh

{ [ ! -e /etc/security/opasswd ] || check_file_root_perms /etc/security/opasswd 600; } && \
{ [ ! -e /etc/security/opasswd.old ] || check_file_root_perms /etc/security/opasswd.old 600; } && \
exit $PASS || exit $FAIL
