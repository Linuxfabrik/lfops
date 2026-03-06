source /tmp/lib.sh

check_file_root_perms /etc/issue.net 644 && exit $PASS || exit $FAIL
