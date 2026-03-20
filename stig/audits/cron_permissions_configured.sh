source /tmp/lib.sh      

check_file_root_perms /etc/crontab 600 && exit $PASS || exit $FAIL
