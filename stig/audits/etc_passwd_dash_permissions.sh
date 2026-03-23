source /tmp/lib.sh

check_file_root_perms /etc/passwd- 644 && exit $PASS || exit $FAIL
