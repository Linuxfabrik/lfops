source /tmp/lib.sh

[ ! -e /etc/motd ] && exit $PASS
check_file_root_perms /etc/motd 644 && exit $PASS || exit $FAIL
