source /tmp/lib.sh

check_file_root_perms /etc/group 644 && exit $PASS || exit $FAIL
