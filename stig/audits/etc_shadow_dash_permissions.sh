source /tmp/lib.sh

check_file_root_perms /etc/shadow- 0 && exit $PASS || exit $FAIL
