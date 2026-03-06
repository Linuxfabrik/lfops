source /tmp/lib.sh

check_file_root_perms /etc/shells 644 && exit $PASS || exit $FAIL
